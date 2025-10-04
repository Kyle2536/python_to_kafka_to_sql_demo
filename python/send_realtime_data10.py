from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "traffic_raw"  # Same topic as production

# Fixed values for simulation
PMGID = 6800017
LOCATION = "32.8943,-96.57669"

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

max_records = 10  # Limit to 10 messages
count = 0

print(f"Starting radar data test simulation... Sending {max_records} records.")

try:
    while count < max_records:
        # Simulate radar data
        radar_data = {
            "Timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),
            "PeakSpeed": random.randint(10, 70),
            "Pmgid": PMGID,
            "Direction": random.choice([0, 1]),
            "Location": LOCATION,
            "VehicleCount": 1
        }

        # Send to Kafka
        producer.send(TOPIC_NAME, value=radar_data)
        print(f"[{count + 1}/{max_records}] Sent to Kafka: {radar_data}")

        count += 1
        time.sleep(1)  # 1-second delay between messages

    print(f"Finished sending {max_records} records.")

except Exception as e:
    print(f"Error occurred: {e}")
finally:
    producer.close()
    print("Kafka producer closed.")
