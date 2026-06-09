import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.nlp.disruption_detector import detect_disruptions, get_headlines
from src.scoring.severity_scorer import score_severity
from src.forecasting.inventory_forecast import forecast_inventory

# Page config
st.set_page_config(
    page_title="Supply Chain Early Warning System",
    page_icon="🚨",
    layout="wide"
)

# Title
st.title("🚨 Supply Chain Early Warning System")
st.markdown("*Real-time disruption detection and inventory impact forecasting*")
st.divider()

# Fetch data
with st.spinner("Fetching live data..."):
    headlines = get_headlines()
    disruptions = detect_disruptions(headlines)
    
    scored = []
    for d in disruptions:
        score = score_severity(d)
        scored.append({
            "headline": d["headline"],
            "keywords": ", ".join(d["keywords"]),
            "severity": score,
            "alert": "🔴 CRITICAL" if score >= 7 else "🟡 WARNING" if score >= 5 else "🟢 LOW"
        })

# --- ALERTS SECTION ---
st.header("🚨 Active Alerts")

critical = [s for s in scored if s["severity"] >= 7]

if critical:
    for c in critical:
        st.error(f"**{c['alert']}** — Score: {c['severity']}/10")
        st.write(f"📰 {c['headline']}")
        
        with st.expander("View 3-Week Inventory Forecast"):
            forecast = forecast_inventory(c["severity"], c["headline"])
            future = forecast.tail(21)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
            future.columns = ["Date", "Predicted", "Low", "High"]
            
            fig = px.line(future, x="Date", y="Predicted",
                         title="Projected Inventory Level (Next 3 Weeks)",
                         labels={"Predicted": "Inventory Units"})
            fig.add_scatter(x=future["Date"], y=future["Low"],
                          mode="lines", name="Worst Case",
                          line=dict(dash="dash", color="red"))
            fig.add_scatter(x=future["Date"], y=future["High"],
                          mode="lines", name="Best Case",
                          line=dict(dash="dash", color="green"))
            st.plotly_chart(fig, use_container_width=True)
else:
    st.success("✅ No critical alerts at this time.")

# --- DISRUPTIONS TABLE ---
st.divider()
st.header("📰 Detected Disruptions")

if scored:
    df = pd.DataFrame(scored)
    df = df.rename(columns={
        "headline": "Headline",
        "keywords": "Keywords",
        "severity": "Severity Score",
        "alert": "Status"
    })
    st.dataframe(df, use_container_width=True)
else:
    st.info("No disruptions detected in current headlines.")

# --- WEATHER SECTION ---
st.divider()
st.header("🌤️ Major Port Weather")

import requests
from dotenv import load_dotenv
load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
ports = ["Shanghai", "Rotterdam", "Los Angeles", "Singapore", "Dubai"]

weather_data = []
for port in ports:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": port,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = requests.get(url, params=params)
    data = response.json()
    weather_data.append({
        "Port": port,
        "Weather": data["weather"][0]["description"].title(),
        "Temperature (°C)": data["main"]["temp"],
        "Wind Speed (m/s)": data["wind"]["speed"]
    })

weather_df = pd.DataFrame(weather_data)
st.dataframe(weather_df, use_container_width=True)

# --- WORLD MAP ---
st.divider()
st.header("🗺️ Global Port Locations")

port_coords = pd.DataFrame({
    "Port": ["Shanghai", "Rotterdam", "Los Angeles", "Singapore", "Dubai"],
    "lat": [31.2304, 51.9225, 34.0522, 1.3521, 25.2048],
    "lon": [121.4737, 4.4792, -118.2437, 103.8198, 55.2708]
})

fig_map = px.scatter_geo(
    port_coords,
    lat="lat",
    lon="lon",
    text="Port",
    title="Monitored Ports",
    projection="natural earth"
)
fig_map.update_traces(marker=dict(size=12, color="red"))
st.plotly_chart(fig_map, use_container_width=True)

# Footer
st.divider()
st.caption("Data sources: NewsAPI • OpenWeatherMap • AISStream | Built with Streamlit + Prophet")
