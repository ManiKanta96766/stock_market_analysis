# Complete Service Analysis - Stock Market Analysis Project

## Overview
This document provides a comprehensive breakdown of all services used in the stock_market_analysis big data project, including their configurations, dependencies, ports, logs, and inter-service communication patterns.

---

## 1. HADOOP / HDFS

### Start/Stop Scripts
- **Start Script**: `stock_market_analysis/hadoop/start-hadoop.bat`
- **Stop Script**: `stock_market_analysis/hadoop/stop-hadoop.bat`
- **WSL Scripts**:
  - Start: `/usr/local/hadoop/sbin/start-dfs.sh` (HDFS)
  - Start: `/usr/local/hadoop/sbin/start-yarn.sh` (YARN)
  - Stop: `/usr/local/hadoop/sbin/stop-yarn.sh`
  - Stop: `/usr/local/hadoop/sbin/stop-dfs.sh`

### Ports Used
- **NameNode RPC**: 9000 (default)
- **NameNode Web UI**: 9870 (Hadoop 3.x) or 50070 (Hadoop 2.x)
- **DataNode**: 9866 (default)
- **Secondary NameNode**: 9868 (default)
- **ResourceManager Web UI**: 8088 (YARN)
- **NodeManager**: 8042 (default)
- **History Server**: 19888 (default)

### Environment Variables
- `HADOOP_HOME`: `/usr/local/hadoop` (assumed from script paths)
- `HADOOP_CONF_DIR`: `$HADOOP_HOME/etc/hadoop` (standard)
- `JAVA_HOME`: Required (JDK path)
- `HDFS_USER`: `hdfs` (typical default)

### Logs Folder Paths
- **HDFS Logs**: `/usr/local/hadoop/logs/` (standard installation)
- **YARN Logs**: `/usr/local/hadoop/logs/` (standard installation)
- **Application Logs**: `$HADOOP_HOME/logs/userlogs/` (YARN application logs)

### Dependencies
- **Java JDK**: Required (typically Java 8 or 11)
- **SSH**: Required for cluster management
- **ZooKeeper**: Optional (for High Availability NameNode)

### Configuration Files and Paths
- **core-site.xml**: `/usr/local/hadoop/etc/hadoop/core-site.xml`
  - Defines HDFS filesystem URI, default replication factor
- **hdfs-site.xml**: `/usr/local/hadoop/etc/hadoop/hdfs-site.xml`
  - NameNode and DataNode configurations
- **yarn-site.xml**: `/usr/local/hadoop/etc/hadoop/yarn-site.xml`
  - ResourceManager and NodeManager settings
- **mapred-site.xml**: `/usr/local/hadoop/etc/hadoop/mapred-site.xml`
  - MapReduce framework configurations
- **hadoop-env.sh**: `/usr/local/hadoop/etc/hadoop/hadoop-env.sh`
  - Environment variables for Hadoop daemons

### Inter-Service Communication Assumptions
- **HDFS** serves as the primary storage layer for:
  - Spark jobs (reading/writing data)
  - HBase (storing table data)
- **YARN** manages resources for:
  - Spark applications (if running in YARN mode)
  - MapReduce jobs
- **Startup Order**: Must start before HBase and Spark (if using HDFS storage)

---

## 2. SPARK MASTER

### Start/Stop Scripts
- **Start Script**: `stock_market_analysis/spark/start-master.bat`
- **Stop Script**: `stock_market_analysis/spark/stop-spark.bat` (stops master and workers)
- **WSL Script**: `/opt/spark/sbin/start-master.sh`
- **Stop WSL Script**: `/opt/spark/sbin/stop-master.sh`

### Ports Used
- **Master RPC**: 7077 (explicitly configured in worker scripts)
- **Master Web UI**: 8080 (referenced in Streamlit app)
- **Master REST API**: 6066 (default)
- **Master Internal**: 7078 (default, for internal communication)

### Environment Variables
- `SPARK_HOME`: `/opt/spark` (from script paths)
- `SPARK_CONF_DIR`: `$SPARK_HOME/conf` (standard)
- `JAVA_HOME`: Required
- `PYSPARK_PYTHON`: Python interpreter path (for PySpark)
- `SPARK_MASTER_HOST`: `localhost` (from worker connection strings)
- `SPARK_MASTER_PORT`: `7077` (from worker connection strings)

### Logs Folder Paths
- **Master Logs**: `/opt/spark/logs/` (standard installation)
- **Application Logs**: `$SPARK_HOME/work/` (worker directories)
- **Driver Logs**: Application-specific (where Spark job is submitted)

### Dependencies
- **Java JDK**: Required
- **Hadoop**: Optional (for HDFS integration)
- **Python**: Required (for PySpark jobs)
- **Scala**: Required (for Spark core)

### Configuration Files and Paths
- **spark-defaults.conf**: `/opt/spark/conf/spark-defaults.conf`
  - Default Spark configurations (master URL, executor memory, etc.)
- **spark-env.sh**: `/opt/spark/conf/spark-env.sh`
  - Environment variables (JAVA_HOME, SPARK_HOME, etc.)
- **log4j2.properties**: `/opt/spark/conf/log4j2.properties`
  - Logging configuration
- **masters**: `/opt/spark/conf/masters` (if using standalone cluster)
- **workers**: `/opt/spark/conf/workers` (worker node list)

### Inter-Service Communication Assumptions
- **Spark Master** coordinates with:
  - **Spark Workers** (via port 7077)
  - **HDFS** (for reading/writing data, if configured)
  - **YARN** (if running in YARN mode)
- **Spark Applications** can connect to:
  - **Kafka** (for streaming data via Spark Streaming)
  - **HBase** (for reading/writing NoSQL data)
- **Connection String**: `spark://localhost:7077` (used by workers and jobs)

---

## 3. SPARK WORKERS

### Start/Stop Scripts
- **Worker 1 Start**: `stock_market_analysis/spark/start-worker1.bat`
- **Worker 2 Start**: `stock_market_analysis/spark/start-worker2.bat`
- **Stop Script**: `stock_market_analysis/spark/stop-spark.bat` (stops all workers)
- **WSL Script**: `/opt/spark/sbin/start-worker.sh spark://localhost:7077`
- **Stop WSL Script**: `/opt/spark/sbin/stop-workers.sh`

### Ports Used
- **Worker Web UI**: 8081, 8082 (default, one per worker)
- **Worker RPC**: 0 (ephemeral, assigned dynamically)
- **Worker Shuffle**: 7337 (default)
- **Worker Block Manager**: 0 (ephemeral)

### Environment Variables
- `SPARK_HOME`: `/opt/spark` (from script paths)
- `SPARK_CONF_DIR`: `$SPARK_HOME/conf` (standard)
- `JAVA_HOME`: Required
- `PYSPARK_PYTHON`: Python interpreter path
- `SPARK_WORKER_DIR`: `$SPARK_HOME/work` (default)
- `SPARK_WORKER_MEMORY`: Memory allocation (configurable)

### Logs Folder Paths
- **Worker Logs**: `/opt/spark/logs/` (standard installation)
- **Application Logs**: `$SPARK_HOME/work/app-*/` (per-application logs)
- **Executor Logs**: `$SPARK_HOME/work/app-*/executor-*/` (executor-specific)

### Dependencies
- **Java JDK**: Required
- **Spark Master**: Must be running (connects to `spark://localhost:7077`)
- **Hadoop**: Optional (for HDFS access)
- **Python**: Required (for PySpark)

### Configuration Files and Paths
- **spark-defaults.conf**: `/opt/spark/conf/spark-defaults.conf`
  - Worker-specific configurations
- **spark-env.sh**: `/opt/spark/conf/spark-env.sh`
  - Environment variables
- **workers**: `/opt/spark/conf/workers`
  - List of worker nodes (if using cluster mode)

### Inter-Service Communication Assumptions
- **Workers** connect to:
  - **Spark Master** at `spark://localhost:7077`
  - **HDFS** (for data storage, if configured)
- **Workers** execute:
  - Tasks assigned by Spark Master
  - Data processing from HDFS, Kafka, or local files
- **Startup Order**: Must start after Spark Master

---

## 4. KAFKA

### Start/Stop Scripts
- **Start Script**: `stock_market_analysis/kafka/start-kafka.bat`
- **Stop Script**: `stock_market_analysis/kafka/stop-kafka.bat`
- **WSL Start Script**: `/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties`
- **WSL Stop Script**: `/usr/local/kafka/bin/kafka-server-stop.sh`

### Ports Used
- **Broker Port**: 9092 (default, configurable in server.properties)
- **ZooKeeper Connection**: 2181 (default, via ZooKeeper)
- **JMX Port**: 9999 (default, for monitoring)

### Environment Variables
- `KAFKA_HOME`: `/usr/local/kafka` (from script paths)
- `KAFKA_CONF_DIR`: `$KAFKA_HOME/config` (standard)
- `KAFKA_LOG_DIRS`: `/tmp/kafka-logs` (default, configurable)
- `JAVA_HOME`: Required
- `KAFKA_HEAP_OPTS`: JVM heap settings (optional)

### Logs Folder Paths
- **Kafka Logs**: `/usr/local/kafka/logs/` (standard installation)
- **Broker Logs**: `$KAFKA_HOME/logs/server.log`
- **Topic Logs**: `$KAFKA_LOG_DIRS/` (data directory for topics)

### Dependencies
- **Java JDK**: Required
- **ZooKeeper**: **REQUIRED** (must be running before Kafka starts)
  - Kafka uses ZooKeeper for:
    - Broker coordination
    - Topic metadata
    - Leader election
    - Consumer group management

### Configuration Files and Paths
- **server.properties**: `/usr/local/kafka/config/server.properties`
  - Broker ID, port, log directories, ZooKeeper connection
  - Key settings:
    - `broker.id=0`
    - `listeners=PLAINTEXT://localhost:9092`
    - `log.dirs=/tmp/kafka-logs`
    - `zookeeper.connect=localhost:2181`
- **producer.properties**: `/usr/local/kafka/config/producer.properties`
  - Producer configurations (optional)
- **consumer.properties**: `/usr/local/kafka/config/consumer.properties`
  - Consumer configurations (optional)

### Inter-Service Communication Assumptions
- **Kafka** depends on:
  - **ZooKeeper** (must start first, port 2181)
- **Kafka** provides data to:
  - **Spark Streaming** (for real-time processing)
  - **Other consumers** (via Kafka Consumer API)
- **Startup Order**: Must start ZooKeeper before Kafka

---

## 5. ZOOKEEPER

### Start/Stop Scripts
- **Start Script**: `stock_market_analysis/kafka/start-zookepper.bat` (note: typo in filename)
- **Stop Script**: `stock_market_analysis/kafka/stop-kafka.bat` (includes ZooKeeper stop)
- **WSL Start Script**: `/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties`
- **WSL Stop Script**: `/usr/local/kafka/bin/zookeeper-server-stop.sh`

### Ports Used
- **Client Port**: 2181 (default, used by Kafka and HBase)
- **Leader Election**: 2888 (default)
- **Peer Communication**: 3888 (default)
- **Admin Server**: 8080 (default, may conflict with Spark UI)

### Environment Variables
- `ZOOKEEPER_HOME`: `/usr/local/kafka` (ZooKeeper bundled with Kafka)
- `ZOOKEEPER_CONF_DIR`: `$ZOOKEEPER_HOME/config` (standard)
- `ZOO_LOG_DIR`: `/usr/local/kafka/logs` (default)
- `JAVA_HOME`: Required
- `ZOOCFGDIR`: `$ZOOKEEPER_HOME/config` (alternative)

### Logs Folder Paths
- **ZooKeeper Logs**: `/usr/local/kafka/logs/` (standard installation)
- **Data Logs**: `$ZOOKEEPER_DATA_DIR/version-2/` (transaction logs)
- **Snapshot Directory**: `$ZOOKEEPER_DATA_DIR/version-2/` (data snapshots)

### Dependencies
- **Java JDK**: Required
- **No external dependencies** (standalone service)

### Configuration Files and Paths
- **zookeeper.properties**: `/usr/local/kafka/config/zookeeper.properties`
  - Client port, data directory, tick time
  - Key settings:
    - `clientPort=2181`
    - `dataDir=/tmp/zookeeper`
    - `tickTime=2000`

### Inter-Service Communication Assumptions
- **ZooKeeper** coordinates:
  - **Kafka** (broker metadata, leader election)
  - **HBase** (region server coordination, master election)
  - **Hadoop** (optional, for NameNode High Availability)
- **Startup Order**: Must start **FIRST** (before Kafka and HBase)

---

## 6. HBASE

### Start/Stop Scripts
- **Start Script**: `stock_market_analysis/hbase/start-hbase.bat`
- **Stop Script**: `stock_market_analysis/hbase/stop-hbase.bat`
- **WSL Script**: `/usr/local/hbase/bin/start-hbase.sh`
- **WSL Stop Script**: `/usr/local/hbase/bin/stop-hbase.sh`

### Ports Used
- **Master Port**: 16000 (default)
- **Master Web UI**: 16010 (default)
- **RegionServer Port**: 16020 (default)
- **RegionServer Web UI**: 16030 (default)
- **REST API**: 8080 (default, may conflict with Spark UI)
- **Thrift Server**: 9090 (default)

### Environment Variables
- `HBASE_HOME`: `/usr/local/hbase` (from script paths)
- `HBASE_CONF_DIR`: `$HBASE_HOME/conf` (standard)
- `JAVA_HOME`: Required
- `HBASE_HEAPSIZE`: JVM heap settings (optional)
- `HBASE_MANAGES_ZK`: `true` or `false` (whether HBase manages ZooKeeper)

### Logs Folder Paths
- **HBase Logs**: `/usr/local/hbase/logs/` (standard installation)
- **Master Logs**: `$HBASE_HOME/logs/hbase-*-master-*.log`
- **RegionServer Logs**: `$HBASE_HOME/logs/hbase-*-regionserver-*.log`
- **ZooKeeper Logs**: `$HBASE_HOME/logs/` (if HBase manages ZooKeeper)

### Dependencies
- **Java JDK**: Required
- **HDFS**: **REQUIRED** (HBase stores data in HDFS)
- **ZooKeeper**: **REQUIRED** (for coordination)
  - Can use bundled ZooKeeper or external ZooKeeper

### Configuration Files and Paths
- **hbase-site.xml**: `/usr/local/hbase/conf/hbase-site.xml`
  - HDFS root directory, ZooKeeper quorum, region server settings
  - Key settings:
    - `hbase.rootdir=hdfs://localhost:9000/hbase`
    - `hbase.zookeeper.quorum=localhost`
    - `hbase.zookeeper.property.clientPort=2181`
- **hbase-env.sh**: `/usr/local/hbase/conf/hbase-env.sh`
  - Environment variables (JAVA_HOME, HBASE_HEAPSIZE, etc.)
- **regionservers**: `/usr/local/hbase/conf/regionservers`
  - List of region server hosts

### Inter-Service Communication Assumptions
- **HBase** depends on:
  - **HDFS** (must be running, stores all table data)
  - **ZooKeeper** (must be running, for coordination)
- **HBase** provides data to:
  - **Spark** (via HBase connector for reading/writing)
  - **Applications** (via REST API, Thrift, or Java API)
- **Startup Order**: Must start after HDFS and ZooKeeper

---

## 7. STREAMLIT

### Start/Stop Scripts
- **Start Script**: `stock_market_analysis/auto_start.bat` (includes Streamlit)
  - Command: `cd streamlit-ui && streamlit run app.py`
- **Stop Script**: `stock_market_analysis/auto_stop.bat`
  - Kills all `python.exe` processes (may affect other Python apps)

### Ports Used
- **Streamlit Server**: 8501 (default)
- **WebSocket**: Same port as server (for real-time updates)

### Environment Variables
- `STREAMLIT_SERVER_PORT`: `8501` (default, configurable)
- `STREAMLIT_BROWSER_GATHER_USAGE_STATS`: `true` or `false`
- `STREAMLIT_SERVER_ADDRESS`: `localhost` (default)
- `PYTHONPATH`: May need to include project directories

### Logs Folder Paths
- **Streamlit Logs**: `~/.streamlit/logs/` (user home directory)
- **Application Logs**: Console output (where `streamlit run` is executed)
- **Error Logs**: `~/.streamlit/logs/streamlit.log`

### Dependencies
- **Python**: Required (Python 3.7+)
- **Streamlit Library**: `pip install streamlit`
- **PySpark**: Required (for Spark job execution)
- **subprocess**: Python standard library (used in app.py)

### Configuration Files and Paths
- **config.toml**: `~/.streamlit/config.toml` (user-specific)
  - Server settings, theme, browser options
- **app.py**: `stock_market_analysis/streamlit-ui/app.py`
  - Main application file
  - Triggers: `../spark-job/advanced_stock_pipeline.py`

### Inter-Service Communication Assumptions
- **Streamlit** triggers:
  - **Spark Jobs** (via subprocess, runs `advanced_stock_pipeline.py`)
- **Streamlit** references:
  - **Spark UI** at `http://localhost:8080` (for monitoring)
- **Note**: The advanced pipeline uses `local[*]` mode, not connecting to Spark Master
- **Simple job** uses `spark://localhost:7077` (connects to Spark Master)

---

## SERVICE STARTUP ORDER

Based on dependencies and scripts:

1. **ZooKeeper** (must start first)
2. **Hadoop/HDFS** (storage layer)
3. **Kafka** (depends on ZooKeeper)
4. **HBase** (depends on HDFS and ZooKeeper)
5. **Spark Master** (can start independently)
6. **Spark Workers** (depend on Spark Master)
7. **Streamlit** (can start independently, triggers Spark jobs)

---

## ADDITIONAL NOTES

### WSL Integration
- All services except Streamlit run inside **WSL (Windows Subsystem for Linux)**
- Scripts use `wsl bash -c` to execute Linux commands from Windows
- Paths are Linux paths (e.g., `/usr/local/hadoop`, `/opt/spark`)

### Configuration File Locations
- Configuration files are **NOT** in the project directory
- They are in standard installation locations within WSL:
  - Hadoop: `/usr/local/hadoop/etc/hadoop/`
  - Spark: `/opt/spark/conf/`
  - Kafka: `/usr/local/kafka/config/`
  - HBase: `/usr/local/hbase/conf/`

### Port Conflicts
- **Port 8080**: Used by both Spark Master Web UI and potentially HBase REST API
- **Port 2181**: Used by ZooKeeper (shared by Kafka and HBase)
- **Port 9092**: Kafka broker (standard)

### Data Paths
- **HDFS Data**: Stored in HDFS (typically `/hbase` for HBase tables)
- **Kafka Data**: `/tmp/kafka-logs/` (default, configurable)
- **ZooKeeper Data**: `/tmp/zookeeper/` (default, configurable)
- **Spark Job Data**: `file:///C:/Users/MANIKANTA/OneDrive/Desktop/stock_market_analysis/spark-job/stocks.csv` (hardcoded path in advanced_stock_pipeline.py)

### Environment Assumptions
- **Java**: Must be installed in WSL
- **Python**: Must be installed (both Windows and WSL if needed)
- **WSL**: Must be configured and accessible
- **Network**: All services assume `localhost` (single-machine setup)

---

## TROUBLESHOOTING CHECKLIST

1. **Check WSL is running**: `wsl --list --verbose`
2. **Check Java**: `wsl java -version`
3. **Check ports are free**: `netstat -an | findstr "8080 7077 2181 9092"`
4. **Check service logs**: Navigate to log directories in WSL
5. **Verify startup order**: Follow the dependency chain
6. **Check configuration files**: Verify paths and settings in WSL

---

*Generated: 2025-01-24*
*Project: stock_market_analysis*

