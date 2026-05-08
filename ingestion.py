"""import requests
from datetime import datetime
import time
from kafka import KafkaProducer
import json

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka ✅")
        break
    except Exception as e:
        print("Waiting for Kafka...", e)
        time.sleep(5)

URL = "https://api.open-meteo.com/v1/forecast?latitude=14.68&longitude=77.60&hourly=temperature_2m,relative_humidity_2m,precipitation,windspeed_10m"

def fetch_weather():
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        index = int(time.time()) % len(data["hourly"]["time"])
        return {
            "location": "Anantapur",
            "timestamp": data["hourly"]["time"][index],
            "temperature": data["hourly"]["temperature_2m"][index],
            "humidity": data["hourly"]["relative_humidity_2m"][index],
            "precipitation": data["hourly"]["precipitation"][index],
            "wind_speed": data["hourly"]["windspeed_10m"][index]
        }
    except Exception as e:
        print("❌ API ERROR:", e)
        return None

def calculate_risk(record):
    rain = record["precipitation"]
    wind = record["wind_speed"]
    humidity = record["humidity"]
    risk_score = (0.4 * rain) + (0.3 * wind) + (0.3 * humidity)
    if risk_score > 70:
        risk = "High"
    elif risk_score > 40:
        risk = "Moderate"
    else:
        risk = "Low"
    record["risk_score"] = round(risk_score, 2)
    record["risk_level"] = risk
    return record

while True:
    print("\n🔄 Fetching weather...")
    weather = fetch_weather()
    if weather is None:
        print("⚠️ Skipping iteration...")
        time.sleep(5)
        continue
    print("📡 Raw Data:", weather)
    result = calculate_risk(weather)
    print("⚙️ Processed:", result)
    producer.send('weather-topic', key=b'weather', value=result)
    producer.flush()
    print("🚀 Sent to Kafka")
    time.sleep(5)"""

""""

import random
import json
import time
from datetime import datetime
from kafka import KafkaProducer

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka ✅")
        break
    except Exception as e:
        print("Waiting for Kafka...", e)
        time.sleep(5)

def generate_weather():
    # Randomly pick a scenario
    scenario = random.choice(["normal", "normal", "moderate", "high", "critical"])
    
    if scenario == "normal":
        precipitation = round(random.uniform(0, 5), 2)
        wind_speed = round(random.uniform(2, 15), 1)
        humidity = round(random.uniform(20, 50), 1)
    elif scenario == "moderate":
        precipitation = round(random.uniform(10, 30), 2)
        wind_speed = round(random.uniform(20, 40), 1)
        humidity = round(random.uniform(50, 70), 1)
    elif scenario == "high":
        precipitation = round(random.uniform(40, 70), 2)
        wind_speed = round(random.uniform(50, 70), 1)
        humidity = round(random.uniform(70, 85), 1)
    else:  # critical
        precipitation = round(random.uniform(80, 120), 2)
        wind_speed = round(random.uniform(80, 120), 1)
        humidity = round(random.uniform(85, 100), 1)

    hour = datetime.now().hour
    base_temp = 28 + 10 * abs((hour - 14) / 14 - 1)

    return {
        "location": "Anantapur",
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "temperature": round(base_temp + random.uniform(-2, 2), 1),
        "humidity": humidity,
        "precipitation": precipitation,
        "wind_speed": wind_speed
    }

def calculate_risk(record):
    rain = record["precipitation"]
    wind = record["wind_speed"]
    humidity = record["humidity"]
    risk_score = (0.4 * rain) + (0.3 * wind) + (0.3 * humidity)
    if risk_score > 70:
        risk = "High"
    elif risk_score > 40:
        risk = "Moderate"
    else:
        risk = "Low"
    record["risk_score"] = round(risk_score, 2)
    record["risk_level"] = risk
    return record

while True:
    weather = generate_weather()
    result = calculate_risk(weather)
    print("🚀 Sending:", result)
    producer.send('weather-topic', key=b'weather', value=result)
    producer.flush()
    time.sleep(3)
"""


"""import requests
import json
import time
from datetime import datetime
from kafka import KafkaProducer

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka ✅")
        break
    except Exception as e:
        print("Waiting for Kafka...", e)
        time.sleep(5)

URL = "https://api.open-meteo.com/v1/forecast?latitude=14.68&longitude=77.60&hourly=temperature_2m,relative_humidity_2m,precipitation,windspeed_10m"

def fetch_weather():
    try:
        response = requests.get(URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        now = datetime.now().strftime("%Y-%m-%dT%H:00")
        times = data["hourly"]["time"]
        index = next((i for i, t in enumerate(times) if t.startswith(now)), 0)
        return {
            "location": "Anantapur",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
            "temperature": data["hourly"]["temperature_2m"][index],
            "humidity": data["hourly"]["relative_humidity_2m"][index],
            "precipitation": data["hourly"]["precipitation"][index],
            "wind_speed": data["hourly"]["windspeed_10m"][index]
        }
    except Exception as e:
        print("❌ API ERROR:", e)
        return None

def calculate_risk(record):
    rain = record["precipitation"]
    wind = record["wind_speed"]
    humidity = record["humidity"]
    risk_score = (0.4 * rain) + (0.3 * wind) + (0.3 * humidity)
    if risk_score > 70:
        risk = "High"
    elif risk_score > 40:
        risk = "Moderate"
    else:
        risk = "Low"
    record["risk_score"] = round(risk_score, 2)
    record["risk_level"] = risk
    return record

while True:
    print("\n🔄 Fetching real weather...")
    weather = fetch_weather()
    if weather:
        result = calculate_risk(weather)
        print("🚀 Sent:", result)
        producer.send('weather-topic', key=b'weather', value=result)
        producer.flush()
    else:
        print("⚠️ Skipping...")
    time.sleep(60)  # fetch every 60 seconds — stays within free limit"""

import requests
import json
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer

# ---------------------------
# LOCATIONS (29 STATES)
# ---------------------------
LOCATIONS = {
    "Andhra Pradesh": ("Anantapur", 14.68, 77.60),
    "Arunachal Pradesh": ("Itanagar", 27.10, 93.62),
    "Assam": ("Guwahati", 26.14, 91.73),
    "Bihar": ("Patna", 25.59, 85.13),
    "Chhattisgarh": ("Raipur", 21.25, 81.63),
    "Goa": ("Panaji", 15.49, 73.82),
    "Gujarat": ("Ahmedabad", 23.02, 72.57),
    "Haryana": ("Chandigarh", 30.73, 76.78),
    "Himachal Pradesh": ("Shimla", 31.10, 77.17),
    "Jharkhand": ("Ranchi", 23.34, 85.31),
    "Karnataka": ("Bangalore", 12.97, 77.59),
    "Kerala": ("Kochi", 9.93, 76.26),
    "Madhya Pradesh": ("Bhopal", 23.26, 77.41),
    "Maharashtra": ("Mumbai", 19.07, 72.87),
    "Manipur": ("Imphal", 24.81, 93.94),
    "Meghalaya": ("Shillong", 25.57, 91.88),
    "Mizoram": ("Aizawl", 23.73, 92.72),
    "Nagaland": ("Kohima", 25.67, 94.11),
    "Odisha": ("Bhubaneswar", 20.30, 85.82),
    "Punjab": ("Ludhiana", 30.90, 75.85),
    "Rajasthan": ("Jaipur", 26.91, 75.79),
    "Sikkim": ("Gangtok", 27.33, 88.62),
    "Tamil Nadu": ("Chennai", 13.08, 80.27),
    "Telangana": ("Hyderabad", 17.38, 78.48),
    "Tripura": ("Agartala", 23.83, 91.28),
    "Uttar Pradesh": ("Lucknow", 26.85, 80.95),
    "Uttarakhand": ("Dehradun", 30.32, 78.03),
    "West Bengal": ("Kolkata", 22.57, 88.36)
}

# ---------------------------
# CONNECT TO KAFKA
# ---------------------------
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers='kafka:9092',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        print("Connected to Kafka ✅")
        break
    except Exception as e:
        print("Waiting for Kafka...", e)
        time.sleep(5)


# ---------------------------
# FETCH WEATHER
# ---------------------------
def fetch_weather(city, lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,precipitation,windspeed_10m"

        response = requests.get(url, timeout=10)
        data = response.json()

        now = datetime.now().strftime("%Y-%m-%dT%H:00")
        times = data["hourly"]["time"]
        idx = next((i for i, t in enumerate(times) if t.startswith(now)), 0)

        return {
            "event_id": str(uuid.uuid4()),
            "location": city,
            "timestamp": datetime.now().isoformat(),
            "temperature": data["hourly"]["temperature_2m"][idx],
            "humidity": data["hourly"]["relative_humidity_2m"][idx],
            "precipitation": data["hourly"]["precipitation"][idx],
            "wind_speed": data["hourly"]["windspeed_10m"][idx],
            "ingested_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"API error for {city}:", e)
        return None


# ---------------------------
# RISK CALCULATION
# ---------------------------
def calculate_risk(record):
    rain = record["precipitation"]
    wind = record["wind_speed"]
    humidity = record["humidity"]

    risk_score = (0.5 * rain) + (0.3 * wind) + (0.2 * humidity)

    if rain > 10:
        risk_score += 15
    if wind > 30:
        risk_score += 10
    if humidity > 80:
        risk_score += 10

    if risk_score > 70:
        risk = "High"
    elif risk_score > 40:
        risk = "Moderate"
    else:
        risk = "Low"

    record["risk_score"] = round(risk_score, 2)
    record["risk_level"] = risk

    return record


# ---------------------------
# STREAM LOOP
# ---------------------------
while True:
    print("\n🌍 Fetching weather for all states...")

    for state, (city, lat, lon) in LOCATIONS.items():
        weather = fetch_weather(city, lat, lon)

        if weather:
            weather["state"] = state
            result = calculate_risk(weather)

            print(f"{state} -> {result['risk_level']}")

            producer.send(
                'weather-topic',
                key=state.encode('utf-8'),
                value=result
            )

    producer.flush()
    time.sleep(120)