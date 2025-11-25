@echo off
echo Stopping HBase...

wsl bash -c "/usr/local/hbase/bin/stop-hbase.sh"

pause
