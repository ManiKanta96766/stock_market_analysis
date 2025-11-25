@echo off
echo Starting full Big Data system...

start cmd /k hadoop\start-hadoop.bat
timeout /t 5

start cmd /k kafka\start-zookeeper.bat
timeout /t 5

start cmd /k kafka\start-kafka.bat
timeout /t 5

start cmd /k hbase\start-hbase.bat
timeout /t 5

start cmd /k spark\start-master.bat
timeout /t 5

start cmd /k spark\start-worker1.bat
start cmd /k spark\start-worker2.bat

timeout /t 5

echo Opening Streamlit UI...
start cmd /k "cd streamlit-ui && streamlit run app.py"

echo All services started!
pause
