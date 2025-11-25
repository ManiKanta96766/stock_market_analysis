@echo off
echo Stopping Spark Master & Workers in WSL...
wsl bash -c "/opt/spark/sbin/stop-master.sh"
wsl bash -c "/opt/spark/sbin/stop-workers.sh"
pause
