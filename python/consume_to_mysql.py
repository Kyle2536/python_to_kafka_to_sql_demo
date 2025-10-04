from kafka import KafkaConsumer
import json
import mysql.connector

# -----------------------
# Kafka setup
# -----------------------
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "traffic_aggregated"

# -----------------------
# MySQL setup
# -----------------------
MYSQL_HOST = "richardsonsql.mysql.database.azure.com"       # or Azure host
MYSQL_PORT = 3306              # adjust if using Docker MySQL
MYSQL_USER = "utdsql"
MYSQL_PASSWORD = "Capstone2025!"
MYSQL_DATABASE = "kafka"

# Connect to MySQL
db = mysql.connector.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    database=MYSQL_DATABASE
)
cursor = db.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS traffic_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp VARCHAR(50),
    total_vehicles INT,
    average_speed FLOAT,
    location VARCHAR(50),
    pmgid BIGINT
)
""")
db.commit()

# -----------------------
# Kafka consumer
# -----------------------
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='mysql_consumer_group'
)

print("Consuming aggregated messages and writing to MySQL...")

# -----------------------
# Consume and insert into MySQL
# -----------------------
for message in consumer:
    data = message.value

    cursor.execute("""
        INSERT INTO traffic_data (timestamp, total_vehicles, average_speed, location, pmgid)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["Timestamp"],
        data["TotalVehicles"],
        data["AverageSpeed"],
        data["Location"],
        data["Pmgid"]
    ))

    db.commit()
    print(f"Inserted into MySQL: {data}")
