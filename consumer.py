"""import json
import time
from kafka import KafkaConsumer
from pymongo import MongoClient

while True:
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["disaster_db"]
        collection = db["weather_data"]
        print("Connected to MongoDB ✅")
        break
    except Exception as e:
        print("Waiting for MongoDB...", e)
        time.sleep(5)

while True:
    try:
        consumer = KafkaConsumer(
            'weather-topic',
            bootstrap_servers='localhost:9092',
            auto_offset_reset='earliest',
            group_id='weather-group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("Connected to Kafka ✅")
        break
    except Exception as e:
        print("Waiting for Kafka...", e)
        time.sleep(5)

print("\n📡 Listening to Kafka...\n")
for message in consumer:
    try:
        data = message.value
        collection.insert_one(data)
        print("💾 Stored:", data)
    except Exception as e:
        print("❌ Error:", e)"""

import json
import time
import os
from datetime import datetime
from kafka import KafkaConsumer
from pymongo import MongoClient
from pymongo import MongoClient
import certifi
# -----------------------------
# Environment (Docker/K8s ready)
# -----------------------------
KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://allwinnnn:Allwin%402003@cluster0.wglbpit.mongodb.net/?appName=Cluster0")

# -----------------------------
# MongoDB Connection
# -----------------------------
while True:
    try:
        client = MongoClient(MONGO_URI,tls=True,tlsCAFile=certifi.where())
        db = client["disaster_db"]
        collection = db["weather_data"]

        # ✅ Create index for deduplication (IMPORTANT)
        collection.create_index("event_id", unique=True)

        print("Connected to MongoDB ✅")
        break
    except Exception as e:
        print("Waiting for MongoDB...", e)
        time.sleep(5)

# -----------------------------
# Kafka Connection
# -----------------------------
# -----------------------------
# Kafka Connection
# -----------------------------
while True:
    try:
        
        consumer = KafkaConsumer(
            'weather-topic',
            bootstrap_servers=KAFKA_SERVER,
            auto_offset_reset='latest',
            enable_auto_commit=False,
            group_id='demo-group-' + str(time.time()),
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        print("Connected to Kafka ✅")
        break

    except Exception as e:
        print("Waiting for Kafka...", e)
        time.sleep(5)

# -----------------------------
# Consume Messages
# -----------------------------
for message in consumer:
    try:
        data = message.value

        # ✅ Add processing timestamp
        data["processed_at"] = datetime.now().isoformat()

        # ✅ Ensure state exists (new multi-state pipeline)
        if "state" not in data:
            data["state"] = "Unknown"

        # ✅ Deduplicate (idempotent write)
        if "event_id" in data:
            collection.update_one(
                {"event_id": data["event_id"]},
                {"$set": data},
                upsert=True
            )
        else:
            collection.insert_one(data)

        # ✅ Better logging (VERY IMPORTANT FOR DEMO)
        print(f"""
💾 Stored Event
🏳 State   : {data.get('state')}
📍 Location: {data.get('location')}
🌡 Temp    : {data.get('temperature')} °C
💧 Humidity: {data.get('humidity')} %
🌧 Rain    : {data.get('precipitation')} mm
⚠ Risk    : {data.get('risk_level')} ({data.get('risk_score')})
""")

    except Exception as e:
        print("❌ Error processing message:", e)