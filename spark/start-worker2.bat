@echo off
echo Starting Spark Worker 2 in WSL...
wsl bash -c "/opt/spark/sbin/start-worker.sh spark://localhost:7077"
pause
