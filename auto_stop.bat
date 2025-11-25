@echo off
echo Stopping ALL Big Data Services...

echo Killing Hadoop...
taskkill /IM java.exe /F >nul 2>&1
taskkill /IM Hadoop.exe /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq Hadoop*" /F >nul 2>&1

echo Killing Kafka & Zookeeper...
taskkill /FI "WINDOWTITLE eq kafka*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq zookeeper*" /F >nul 2>&1

echo Killing HBase...
taskkill /FI "WINDOWTITLE eq hbase*" /F >nul 2>&1

echo Killing Spark Master & Workers...
taskkill /FI "WINDOWTITLE eq spark*" /F >nul 2>&1
taskkill /IM spark-class2.cmd /F >nul 2>&1
taskkill /IM spark-class.cmd /F >nul 2>&1

echo Killing Streamlit...
taskkill /IM python.exe /F >nul 2>&1

echo Closing all CMD windows started by start.cmd...
taskkill /IM cmd.exe /F >nul 2>&1

echo All services stopped!
pause
