import psutil as p
import pymysql as sql
import time
import sys

def get_sql_connection(host="0.0.0.0", username="root", password="my-secret-pw", db="data_collection"):
    return sql.connect(host, username, password, db)

db = get_sql_connection()

if len(sys.argv) != 2:
    print("Usage : python3 monitor_service.py <node_id>")
    exit()
processes = {}

runner = db.cursor()
# docker run -d -P -p 7707:7707 -p 8080:8080 --name ssh_test_master ssh_master
# docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d -p 3306:3306 mysql
create_statement = """ 
    CREATE TABLE IF NOT EXISTS CPU_DATA (
        CONTEXT_SWITCHES INT,
        INTERRUPTS INT,
        SOFT_INTERRUPTS INT,
        DISK_R INT,
        DISK_R_BYTES INT,
        DISK_W INT,
        DISK_W_BYTES INT,
        CPU_PERCENT FLOAT,
        VIRTUAL_MEMORY INT,
        NODE_ID INT
    )
"""

def enter_values(processes, node_id=0) :
    cstat = p.cpu_stats()
    dstat = p.disk_io_counters()
    if "ctx" not in processes :
        processes["ctx"] = cstat[0]
        processes["intr"] = cstat[1]
        processes["soft_intr"] = cstat[2]
        processes["disk_r"] = dstat[0]
        processes["disk_rb"] = dstat[2]
        processes["disk_w"] = dstat[1]
        processes["disk_wb"] = dstat[3]
        processes["cpu"] = p.cpu_percent()
        processes["vmem"] = p.virtual_memory()[2]
        print(processes)
        return "", processes
    enter_statement = """ 
        INSERT INTO CPU_DATA ( CONTEXT_SWITCHES, INTERRUPTS, SOFT_INTERRUPTS, DISK_R, DISK_R_BYTES, DISK_W, DISK_W_BYTES, CPU_PERCENT, VIRTUAL_MEMORY            
        ) VALUES ("""+str(cstat[0] - processes["ctx"])+","+str(cstat[1] - processes["intr"])+","+str(cstat[2] - processes["soft_intr"])+","+str(dstat[0] - processes["disk_r"])+","+str(dstat[2] - processes["disk_rb"])+","+str(dstat[1] - processes["disk_w"])+","+str(dstat[3] - processes["disk_wb"])+","+str(p.cpu_percent() - processes["cpu"])+","+str(p.virtual_memory()[2] - processes["vmem"])+","+node_id+")"
    processes["ctx"] = cstat[0]
    processes["intr"] = cstat[1]
    processes["soft_intr"] = cstat[2]
    processes["disk_r"] = dstat[0]
    processes["disk_rb"] = dstat[2]
    processes["disk_w"] = dstat[1]
    processes["disk_wb"] = dstat[3]
    processes["cpu"] = p.cpu_percent()
    processes["vmem"] = p.virtual_memory()[2]
    return enter_statement, processes


runner.execute(create_statement)

while True :
    # print("Entered into db")
    insert_query, processes = enter_values(processes, sys.argv[1])
    if insert_query != "":
        runner.execute(insert_query)
        db.commit()    
    time.sleep(3)