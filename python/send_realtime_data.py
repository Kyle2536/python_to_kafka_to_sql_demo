"""
send_realtime_data.py
---------------------
Sends real-time traffic data to a Kafka topic.

Author: Capstone Team
Date: 2025-10-04
"""

from kafka import KafkaProducer
import json, random, time
from datetime import datetime

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "traffic_raw"

# === Fixed configuration ===
NUM_LOCATIONS = 1000   # total unique locations to simulate
NUM_PMGIDS = 10000     # total unique PMGIDs to simulate

# Pre-generate 1000 unique random locations
locations = [
    f"{random.uniform(32.0, 33.0):.4f},{random.uniform(-97.0, -96.0):.4f}"
    for _ in range(NUM_LOCATIONS)
]

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Streaming raw data to Kafka (Press Ctrl+C to stop)...")

try:
    while True:
        start_time = time.time()

        # Generate current date/time
        now = datetime.now()
        created_at = now.strftime("%Y-%m-%d")            # e.g. "2025-10-04"
        timestamp = now.strftime("%H:%M:%S.%f")[:-3]     # e.g. "22:21:51.228"

        # Build one simulated data record
        data = {
            "created_at": created_at,
            "timestamp": timestamp,
            "PeakSpeed": random.randint(10, 70),
            "Pmgid": random.randint(1, NUM_PMGIDS),
            "Direction": random.choice([0, 1]),
            "Location": random.choice(locations),
            "VehicleCount": 1,
            "GeneratedAt": time.time()
        }

        # Send data to Kafka
        producer.send(TOPIC_NAME, value=data)
        producer.flush()

        elapsed = time.time() - start_time
        print(f"Sent: {data} | Generation time: {elapsed:.4f}s")

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped.")
finally:
    producer.close()
