"""import time
import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title="Disaster Dashboard", layout="wide")
st.title("🌦️ Real-Time Disaster Monitoring Dashboard")

client = MongoClient("mongodb://localhost:27017/")
db = client["disaster_db"]
collection = db["weather_data"]

placeholder = st.empty()

while True:
    data = list(collection.find().sort("_id", -1).limit(100))

    with placeholder.container():
        if not data:
            st.warning("No data found in MongoDB yet...")
        else:
            df = pd.DataFrame(data)
            df = df.drop(columns=["_id"], errors="ignore")
            df = df.iloc[::-1].reset_index(drop=True)
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            latest = df.iloc[-1]

            # Alert
            if latest["risk_level"] == "High":
                st.error("🚨 HIGH RISK ALERT! Possible flood/cyclone conditions!")
            elif latest["risk_level"] == "Moderate":
                st.warning("⚠️ Moderate Risk — Monitor conditions closely")
            else:
                st.success("✅ Low Risk — Conditions are normal")

            # Metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("🌡 Temperature (°C)", latest["temperature"])
            col2.metric("💧 Humidity (%)", latest["humidity"])
            col3.metric("🌧 Precipitation (mm)", latest["precipitation"])
            col4.metric("💨 Wind Speed (km/h)", latest["wind_speed"])
            col5.metric("⚠ Risk Score", latest["risk_score"])

            # Risk distribution
            st.subheader("📊 Risk Level Distribution")
            risk_counts = df["risk_level"].value_counts()
            col1, col2, col3 = st.columns(3)
            col1.metric("🟢 Low", risk_counts.get("Low", 0))
            col2.metric("🟡 Moderate", risk_counts.get("Moderate", 0))
            col3.metric("🔴 High", risk_counts.get("High", 0))

            # Charts
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🌡 Temperature Trend")
                st.line_chart(df.set_index("timestamp")["temperature"])
                st.subheader("🌧 Precipitation Trend")
                st.line_chart(df.set_index("timestamp")["precipitation"])
            with col2:
                st.subheader("💨 Wind Speed Trend")
                st.line_chart(df.set_index("timestamp")["wind_speed"])
                st.subheader("⚠ Risk Score Trend")
                st.line_chart(df.set_index("timestamp")["risk_score"])

            # Table
            st.subheader("📄 Latest 100 Records")
            st.dataframe(df.tail(100), use_container_width=True)

            st.caption(f"🔄 Last updated: {datetime.now().strftime('%H:%M:%S')}" if False else f"🔄 Total records in DB: {collection.count_documents({})}")

    time.sleep(3)"""
import streamlit as st
import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime
import time
import certifi
# ---------------------------
# Config
# ---------------------------
st.set_page_config(page_title="Disaster Dashboard", layout="wide")
st.title("🌦️ Real-Time Disaster Monitoring Dashboard")

# ---------------------------
# State Coordinates (Heatmap)
# ---------------------------
STATE_COORDS = {
    "Andhra Pradesh": (14.68, 77.60),
    "Arunachal Pradesh": (27.10, 93.62),
    "Assam": (26.14, 91.73),
    "Bihar": (25.59, 85.13),
    "Chhattisgarh": (21.25, 81.63),
    "Goa": (15.49, 73.82),
    "Gujarat": (23.02, 72.57),
    "Haryana": (30.73, 76.78),
    "Himachal Pradesh": (31.10, 77.17),
    "Jharkhand": (23.34, 85.31),
    "Karnataka": (12.97, 77.59),
    "Kerala": (9.93, 76.26),
    "Madhya Pradesh": (23.26, 77.41),
    "Maharashtra": (19.07, 72.87),
    "Manipur": (24.81, 93.94),
    "Meghalaya": (25.57, 91.88),
    "Mizoram": (23.73, 92.72),
    "Nagaland": (25.67, 94.11),
    "Odisha": (20.30, 85.82),
    "Punjab": (30.90, 75.85),
    "Rajasthan": (26.91, 75.79),
    "Sikkim": (27.33, 88.62),
    "Tamil Nadu": (13.08, 80.27),
    "Telangana": (17.38, 78.48),
    "Tripura": (23.83, 91.28),
    "Uttar Pradesh": (26.85, 80.95),
    "Uttarakhand": (30.32, 78.03),
    "West Bengal": (22.57, 88.36)
}

# ---------------------------
# MongoDB
# ---------------------------
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(

    MONGO_URI,

    tls=True,

    tlsCAFile=certifi.where()

)
db = client["disaster_db"]
collection = db["weather_data"]

# ---------------------------
# Fetch Data
# ---------------------------
data = list(collection.find().sort("_id", -1).limit(500))

if not data:
    st.warning("No data found in MongoDB yet...")

else:
    df = pd.DataFrame(data)
    df = df.drop(columns=["_id"], errors="ignore")

    # Sort properly
    if "ingested_at" in df.columns:
        df = df.sort_values("ingested_at")
    else:
        df = df.iloc[::-1]

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # ---------------------------
    # 🌍 Latest Per State
    # ---------------------------
    st.subheader("📍 Latest Data Per State")

    latest_per_state = (
        df.sort_values("timestamp")
          .groupby("state")
          .tail(1)
    )

    st.dataframe(latest_per_state, use_container_width=True)

    # ---------------------------
    # 🗺️ India Heatmap
    # ---------------------------
    st.subheader("🗺️ India Risk Heatmap")

    map_df = latest_per_state.copy()

    map_df["latitude"] = map_df["state"].map(lambda x: STATE_COORDS.get(x, (None, None))[0])
    map_df["longitude"] = map_df["state"].map(lambda x: STATE_COORDS.get(x, (None, None))[1])

    map_df = map_df.dropna(subset=["latitude", "longitude"])

    st.map(map_df[["latitude", "longitude"]])

    # ---------------------------
    # 🚨 Global Alert
    # ---------------------------
    risk_counts = latest_per_state["risk_level"].value_counts()

    if "High" in risk_counts:
        st.error("🚨 HIGH RISK detected in one or more states!")
    elif "Moderate" in risk_counts:
        st.warning("⚠️ Moderate risk conditions present")
    else:
        st.success("✅ All regions are low risk")

    # ---------------------------
    # 📊 National Risk Distribution
    # ---------------------------
    st.subheader("📊 National Risk Distribution")

    col1, col2, col3 = st.columns(3)
    col1.metric("🟢 Low", risk_counts.get("Low", 0))
    col2.metric("🟡 Moderate", risk_counts.get("Moderate", 0))
    col3.metric("🔴 High", risk_counts.get("High", 0))

    # ---------------------------
    # 🔎 State Filter
    # ---------------------------
    st.subheader("🌍 Select State")

    selected_state = st.selectbox(
        "Choose a state",
        sorted(df["state"].unique())
    )

    state_df = df[df["state"] == selected_state]

    latest = state_df.iloc[-1]

    # ---------------------------
    # 📍 State Header
    # ---------------------------
    st.subheader(f"📍 {selected_state} - {latest['location']}")

    # ---------------------------
    # 📊 Metrics
    # ---------------------------
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🌡 Temperature", latest["temperature"])
    col2.metric("💧 Humidity", latest["humidity"])
    col3.metric("🌧 Rain", latest["precipitation"])
    col4.metric("💨 Wind", latest["wind_speed"])
    col5.metric("⚠ Risk Score", latest["risk_score"])

    # ---------------------------
    # 📈 Charts
    # ---------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌡 Temperature Trend")
        st.line_chart(state_df.set_index("timestamp")["temperature"])

        st.subheader("🌧 Rain Trend")
        st.line_chart(state_df.set_index("timestamp")["precipitation"])

    with col2:
        st.subheader("💨 Wind Trend")
        st.line_chart(state_df.set_index("timestamp")["wind_speed"])

        st.subheader("⚠ Risk Trend")
        st.line_chart(state_df.set_index("timestamp")["risk_score"])

    # ---------------------------
    # 📄 Table
    # ---------------------------
    st.subheader("📄 State Records")
    st.dataframe(state_df.tail(100), use_container_width=True)

    st.caption(f"🔄 Total records: {collection.count_documents({})}")

# ---------------------------
# AUTO REFRESH
# ---------------------------
time.sleep(2)
st.rerun()