@echo off
echo Starting Kafka Broker...

wsl bash -c "/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties"

pause
