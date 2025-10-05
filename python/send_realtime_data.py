from kafka import KafkaProducer
import json, random, time
from datetime import datetime

KAFKA_BROKER = "localhost:9092"
TOPIC_NAME = "traffic_raw"

PMGID = 6800017
LOCATION = "32.8943,-96.57669"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Streaming raw radar data to Kafka... Press Ctrl+C to stop.")

try:
    while True:
        start_time = time.time()  # ⏱ start generation timer

        data = {
            "Timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),
            "PeakSpeed": random.randint(10, 70),
            "Pmgid": PMGID,
            "Direction": random.choice([0, 1]),
            "Location": LOCATION,
            "VehicleCount": 1,
            "GeneratedAt": time.time()  # used for end-to-end timing
        }

        producer.send(TOPIC_NAME, value=data)
        producer.flush()

        elapsed = time.time() - start_time  # ⏱ generation time
        print(f"Sent: {data} | Generation time: {elapsed:.4f}s")

        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped.")
finally:
    producer.close()
