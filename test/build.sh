docker build -t ssh_master .
docker build -t ssh_slave .
docker run -d -P --name ssh_test_master ssh_master
docker run -d -P --name ssh_test_salve ssh_slave
docker port ssh_test_master 22
docker port ssh_test_salve 22
