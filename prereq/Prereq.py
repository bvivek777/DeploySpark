from prereq.Helper import Helper;
from error_handler import Error_Handler as e;

class Prereq :

    def __init__(self):
        super().__init__();
        self.exceptions = [
            e.JavaInstallationFailure,
            e.Pip3InstallationException,
            e.Python3InstallationFailure,
            e.SparkInstallationFailure,
            e.WgetInstallationException
        ]

    def install_prereqs(self, connection, os="ubuntu" ) :
        helper = Helper(connection)
        helper.download_and_install_tar(connection, component="JAVA", os="ubuntu")
        helper.download_and_install_tar(connection, component="SPARK", os="ubuntu")
        helper.install_package(connection, "python3", os)
        helper.install_package(connection, "pip3", os)
        helper.install_package(connection, "psutil", os)
        helper.install_package(connection, "mysql", os)
    
    def load_config(self, connection, config, master=False, node_id=0) :
        try:
            helper = Helper(connection)
            # Create the ssh director for public and private keys
            base_dir = config['base']
            connection.run(" cd "+base_dir+" && mkdir -p .ssh")

            if master:
                print("Loading config for master")
                # for the master node generate the public priv keys and download a copy to local
                d, exists = helper.check_file(connection, base_dir+"/.ssh/", 'id_rsa')
                if not exists :
                    print("Generating ssh keys for master")
                    connection.run("cd "+base_dir+"/.ssh &&"+"ssh-keygen -q -t rsa -N '' <<< id_rsa$'\\n'\\\"y\\\" 2>&1 >/dev/null")   
                print("Downloading RSA files generated")         
                connection.get(base_dir+"/.ssh/id_rsa.pub", "./install_packages/keys/id_rsa.pub", True)
                # Add the worker ips to all the config of spark
                d, exists = helper.check_file(connection, "/opt/spark/conf/", "slaves")
                if not exists:
                    print("Generating worker directory for master")
                    connection.run("cp /opt/spark/conf/slaves.template /opt/spark/conf/slaves")            
                    for workers in config["workers"]:
                        connection.run("echo '"+workers+"' >> /opt/spark/conf/slaves")
            else :
                print("Loading config for worker")
                # upload the ssh config and the authorized keys
                print("Uploading sshd config and authorized keys")
                helper.upload_file(connection, "./install_packages/keys/sshd_config", "/etc/ssh/sshd_config")
                helper.upload_file(connection, "./install_packages/keys/id_rsa.pub", base_dir+"/.ssh/authorized_keys")

            print("adding env to spark config")
            connection.run("echo \"export JAVA_HOME=$JAVA_HOME\" >> /opt/spark/spark-config.sh")
            helper.upload_file(connection, "./monitor/monitor_service.py", base_dir+"/monitor.py")
            print("starting monitor")
            connection.run("nohup python3 monitor.py &> output.log")
        except:
            print("Error loading config")
        
    def start_services(self, connection):
        # Start monitor and spark
        connection.run("cd /opt/spark/sbin && ./start-all.sh")
