import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def fetch_port_weather():
    ports = ["Shanghai", "Rotterdam", "Los Angeles", "Singapore", "Dubai"]
    
    for port in ports:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": port,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        print(f"Port: {port}")
        print(f"Weather: {data['weather'][0]['description']}")
        print(f"Temperature: {data['main']['temp']}°C")
        print(f"Wind Speed: {data['wind']['speed']} m/s")
        print("---")

fetch_port_weather()