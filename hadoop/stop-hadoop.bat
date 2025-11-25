@echo off
echo Stopping Hadoop...

wsl bash -c "/usr/local/hadoop/sbin/stop-yarn.sh"
wsl bash -c "/usr/local/hadoop/sbin/stop-dfs.sh"

echo Hadoop stopped.
pause
