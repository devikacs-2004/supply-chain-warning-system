# 🚨 Supply Chain Early Warning System

A real-time supply chain disruption detection and inventory impact forecasting system built with Python, NLP, and Machine Learning.

🔴 **Live Demo:** https://supply-chain-warning-system-ytznycvaxidfwgxhpctdey.streamlit.app/

---

## 📌 What It Does

Monitors global news, weather, and ship data to detect supply chain disruptions **2-3 weeks before they impact inventory levels.**

- 📰 Fetches live news headlines using NewsAPI
- 🌤️ Monitors weather at 5 major global ports
- 🚢 Tracks live vessel movements via AISStream
- 🧠 Detects disruptions using NLP keyword analysis
- 📊 Scores severity on a 1-10 scale
- 📈 Forecasts inventory impact using Facebook Prophet
- 🚨 Fires critical alerts when severity > 7
- 🗺️ Displays live dashboard with Plotly world map

---

## 🏗️ System Architecture
Data Layer        →  NLP Layer       →  Scoring Layer  →  Forecast Layer  →  Alert Layer  →  Dashboard
NewsAPI              Keyword              Severity          Facebook            Threshold       Streamlit
OpenWeatherMap       Detection            Scoring           Prophet             Alerts          + Plotly
AISStream            (disruption_        (1-10 scale)      (21-day             (severity>7)
detector.py)                          forecast)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Data Ingestion | NewsAPI, OpenWeatherMap, AISStream |
| NLP | Keyword-based disruption detection |
| Scoring | Custom weighted severity function |
| Forecasting | Facebook Prophet |
| Alerts | Custom threshold engine |
| Dashboard | Streamlit + Plotly |
| Language | Python 3.13 |

---

## 📁 Project Structure
supply-chain-warning-system/
│
├── data/
├── notebooks/
├── src/
│   ├── ingestion/
│   │   ├── fetch_news.py
│   │   ├── fetch_weather.py
│   │   ├── fetch_ships.py
│   │   └── pipeline.py
│   ├── nlp/
│   │   └── disruption_detector.py
│   ├── scoring/
│   │   └── severity_scorer.py
│   ├── forecasting/
│   │   └── inventory_forecast.py
│   └── alerts/
│       └── alert_system.py
├── dashboard/
│   └── app.py
├── .env.example
├── requirements.txt
└── README.md

---

## 🚀 Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/devikacs-2004/supply-chain-warning-system.git
cd supply-chain-warning-system
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add API keys**
```bash
cp .env.example .env
# Fill in your real keys in .env
```

**5. Run the dashboard**
```bash
streamlit run dashboard/app.py
```

---

## 👥 Built By

| Name | Role | LinkedIn | GitHub |
|------|------|----------|--------|
| Devika CS | Data pipeline, NLP detection, Ship data, Forecasting | [LinkedIn](www.linkedin.com/in/devika-cs-594511286) | [GitHub](https://github.com/devikacs-2004) |
| Navafa PM | Weather data, Severity scoring, Alert system, Dashboard | [LinkedIn](https://www.linkedin.com/in/navafa-pm-a0233a293) | [GitHub](https://github.com/Navafa-Manaf) |

---

## 📡 Data Sources

- [NewsAPI](https://newsapi.org) — Global news headlines
- [OpenWeatherMap](https://openweathermap.org) — Port weather data
- [AISStream](https://aisstream.io) — Live vessel tracking

---


