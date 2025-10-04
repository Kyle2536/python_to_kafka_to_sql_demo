from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "traffic_raw"  # Updated to match your project pipeline

# Fixed values for simulation
PMGID = 6800017
LOCATION = "32.8943,-96.57669"

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Starting radar data simulation... Press Ctrl+C to stop.")

try:
    while True:
        # Simulate radar data
        radar_data = {
            "Timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),  # e.g., 09/15/2025 03:17:00 PM
            "PeakSpeed": random.randint(10, 70),   # Speed in mph
            "Pmgid": PMGID,                         # Static PMGID
            "Direction": random.choice([0, 1]),     # 0 = one direction, 1 = opposite direction
            "Location": LOCATION,                    # Fixed GPS coordinates
            "VehicleCount": 1                        # Always 1 per record
        }

        # Send to Kafka
        producer.send(TOPIC_NAME, value=radar_data)
        print(f"Sent to Kafka topic '{TOPIC_NAME}': {radar_data}")

        # Simulate 1-second interval between vehicle detections
        time.sleep(1)

except KeyboardInterrupt:
    print("Radar data simulation stopped.")
finally:
    producer.close()
