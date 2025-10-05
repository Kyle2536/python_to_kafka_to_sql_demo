Real-Time Traffic Data Pipeline (Python -> Kafka -> MySQL)

This project simulates radar-sensor traffic data in real time, streams it through Apache Kafka, and stores it in an Azure MySQL database. It’s designed to be reproduced with Docker and Python.

--------------------------------------------------------------------------------
Project Overview
--------------------------------------------------------------------------------
Architecture:
Python Producer (send_realtime_data.py)
        │
        ▼
    Kafka Topic: traffic_raw
        │
        ▼
Python Consumer (consume_to_mysql.py)
        │
        ▼
 Azure MySQL Database (table: raw_data_kafka)

- Producer: generates simulated traffic events every second.
- Kafka: acts as the message broker.
- Consumer: reads each Kafka message and inserts it into Azure MySQL.
- MySQL (Azure): stores raw event data for later analysis.

--------------------------------------------------------------------------------
Requirements
--------------------------------------------------------------------------------
Python ≥ 3.9
Docker Desktop (latest)
Docker Compose (bundled with Docker)
Azure MySQL Server (accessible with valid credentials)
Python packages: kafka-python, mysql-connector-python

Install dependencies:
    pip install kafka-python mysql-connector-python

--------------------------------------------------------------------------------
Docker Setup (Kafka Only)
--------------------------------------------------------------------------------
Create and start the Kafka container:
    docker-compose up -d

Check that Kafka is running:
    docker ps

Expected:
    CONTAINER ID   IMAGE                  STATUS         PORTS
    xxxxxx         bitnami/kafka:latest   Up ...         0.0.0.0:9092->9092/tcp

--------------------------------------------------------------------------------
Azure MySQL Configuration
--------------------------------------------------------------------------------
Hostname:  richardsonsql.mysql.database.azure.com
Port:      3306
Username:  utdsql
Password:  <your-password>
Database:  kafka

Test the connection:
    import mysql.connector
    db = mysql.connector.connect(
        host="richardsonsql.mysql.database.azure.com",
        port=3306,
        user="utdsql",
        password="YOUR_PASSWORD",
        database="kafka",
        ssl_disabled=False
    )
    print("Connected!") if db.is_connected() else print("Connection failed")
    db.close()

--------------------------------------------------------------------------------
Running the Pipeline
--------------------------------------------------------------------------------
1. Start the Kafka consumer:
    python consume_to_mysql.py

Expected:
    Connected to database: kafka
    Consuming raw radar data from Kafka...

2. Start the producer:
    python send_realtime_data.py

This sends continuous traffic samples such as:
    Sent: {'Timestamp': '10/04/2025 04:14:26 PM', 'PeakSpeed': 65, ...}

Stop with Ctrl +C.

Consumer output example:
    Inserted raw data: {...}
    Total pipeline time: 0.47 seconds
    No new messages for 5 seconds — consumer stopped.

--------------------------------------------------------------------------------
Table Schema
--------------------------------------------------------------------------------
Table: raw_data_kafka

Columns:
    id INT AUTO_INCREMENT PRIMARY KEY
    timestamp VARCHAR(50)
    peakspeed INT
    pmgid BIGINT
    direction INT
    location VARCHAR(50)
    vehiclecount INT
    generation_time FLOAT
    total_pipeline_time FLOAT

--------------------------------------------------------------------------------
Testing Direct vs Kafka Performance
--------------------------------------------------------------------------------
Run a direct-to-MySQL test (no Kafka):
    python raw_data_direct.py

Compare:
    total_insert_time (direct)
vs
    total_pipeline_time (Kafka)

--------------------------------------------------------------------------------
Common Commands
--------------------------------------------------------------------------------
Restart Kafka: docker-compose restart kafka
Stop Kafka: docker-compose down
View Kafka logs: docker logs kafka
List topics: docker exec -it kafka kafka-topics.sh --bootstrap-server localhost:9092 --list
Create topic:
    docker exec -it kafka kafka-topics.sh --create --topic traffic_raw --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

--------------------------------------------------------------------------------
Troubleshooting
--------------------------------------------------------------------------------
Consumer stuck -> Waiting for more Kafka messages (auto-stops after 5s inactivity)

