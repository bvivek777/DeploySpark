docker run -d -P -p 7707:7707 -p 8080:8080 --name ssh_test_master ssh_master 
docker run -d -P --name ssh_test_salve ssh_slave