from kafka import KafkaConsumer
import json
import mysql.connector
import time

# Kafka setup
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "traffic_raw"

# MySQL setup
MYSQL_HOST = "richardsonsql.mysql.database.azure.com"
MYSQL_PORT = 3306
MYSQL_USER = "utdsql"
MYSQL_PASSWORD = "Capstone2025!"
MYSQL_DATABASE = "kafka"  # your correct schema name

# Connect to MySQL
db = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = db.cursor()

# Confirm active DB
cursor.execute("SELECT DATABASE();")
print("Connected to database:", cursor.fetchone()[0])

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS raw_data_kafka (
    id INT AUTO_INCREMENT PRIMARY KEY,
    created_at DATE,
    timestamp VARCHAR(15),
    peakspeed INT,
    pmgid BIGINT,
    direction INT,
    location VARCHAR(50),
    vehiclecount INT,
    generation_time FLOAT,
    total_pipeline_time FLOAT
)
""")
db.commit()

# Kafka consumer setup with timeout
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='mysql_raw_consumer',
    consumer_timeout_ms=5000  # 5 seconds of inactivity triggers stop
)


print("Consuming raw data from Kafka and inserting into MySQL (table: raw_data_kafka)")

msg_count = 0
pipeline_start = time.time()  # total pipeline timer

for message in consumer:
    start_total = time.time()
    data = message.value

    gen_time = data.get("GeneratedAt", start_total)
    total_pipeline_time = start_total - gen_time

    cursor.execute("""
        INSERT INTO raw_data_kafka (
            created_at, timestamp, peakspeed, pmgid, direction, location, vehiclecount,
            generation_time, total_pipeline_time
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data["created_at"],
        data["timestamp"],
        data["PeakSpeed"],
        data["Pmgid"],
        data["Direction"],
        data["Location"],
        data["VehicleCount"],
        0.0,
        total_pipeline_time
    ))
    db.commit()

    msg_count += 1
    print(f"Inserted raw data: {data}")
    print(f"⏱ Total pipeline time: {total_pipeline_time:.4f} seconds\n")

print(f"No new messages for 5 seconds — consumer stopped.")
print(f"Total messages processed: {msg_count}")
print(f"Total runtime: {time.time() - pipeline_start:.2f} seconds")

# Clean up
cursor.close()
db.close()
