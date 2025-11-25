@echo off
echo Starting Spark Worker 1 in WSL...
wsl bash -c "/opt/spark/sbin/start-worker.sh spark://localhost:7077"
pause
