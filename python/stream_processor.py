# stream_processor.py
from kafka import KafkaConsumer, KafkaProducer
import json
from datetime import datetime

KAFKA_BROKER = "localhost:9092"
RAW_TOPIC = "traffic_raw"
AGGREGATED_TOPIC = "traffic_aggregated"

consumer = KafkaConsumer(
    RAW_TOPIC,
    bootstrap_servers=[KAFKA_BROKER],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='stream_processor_group'
)

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Stream processor started. Listening for raw traffic data...")

total_speed = 0
total_vehicles = 0

for message in consumer:
    data = message.value
    print("Received raw message:", data)

    total_speed += data["PeakSpeed"]
    total_vehicles += data["VehicleCount"]

    aggregated_data = {
        "Timestamp": datetime.now().strftime("%m/%d/%Y %I:%M:%S %p"),
        "TotalVehicles": total_vehicles,
        "AverageSpeed": round(total_speed / total_vehicles, 2),
        "Location": data["Location"],
        "Pmgid": data["Pmgid"]
    }

    producer.send(AGGREGATED_TOPIC, value=aggregated_data)
    print("Sent aggregated data:", aggregated_data)
