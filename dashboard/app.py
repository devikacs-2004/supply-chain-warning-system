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