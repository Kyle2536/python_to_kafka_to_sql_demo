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

print("Starting 10-sample radar data test...")

total_start = time.time()  # ⏱ Start total timer

for i in range(10):
    start_gen = time.time()  # ⏱ Start generation timer

    data = {
        "Timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        "PeakSpeed": random.randint(10, 70),
        "Pmgid": PMGID,
        "Direction": random.choice([0, 1]),
        "Location": LOCATION,
        "VehicleCount": 1,
        "GeneratedAt": time.time()
    }

    producer.send(TOPIC_NAME, value=data)
    producer.flush()

    gen_time = time.time() - start_gen
    print(f"[{i+1}/10] Sent: {data} | Generation time: {gen_time:.4f}s")

    time.sleep(1)  # mimic real sensor rate

total_elapsed = time.time() - total_start
print(f"\n✅ Finished sending 10 samples.")
print(f"Total time to generate and send all data: {total_elapsed:.4f}s")

producer.close()
