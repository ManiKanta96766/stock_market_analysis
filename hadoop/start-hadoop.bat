@echo off
echo Starting Hadoop inside WSL...

wsl bash -c "/usr/local/hadoop/sbin/start-dfs.sh"
wsl bash -c "/usr/local/hadoop/sbin/start-yarn.sh"

echo Hadoop started via WSL.
pause
