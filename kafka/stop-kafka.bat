@echo off
echo Stopping Kafka...

wsl bash -c "/usr/local/kafka/bin/kafka-server-stop.sh"
wsl bash -c "/usr/local/kafka/bin/zookeeper-server-stop.sh"

pause
