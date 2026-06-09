import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()
# add project root to path

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.ingestion.fetch_news import fetch_supply_chain_news
from src.ingestion.fetch_weather import fetch_port_weather
from src.ingestion.fetch_ships import fetch_ship_data

def run_pipeline():
    print("="*50)
    print("SUPPLY CHAIN EARLY WARNING SYSTEM")
    print("data Ingestion Pipeline Starting...")
    print("="*50)
    print("\nFETCHING NEWS DATA...")
    print("-"*30)

    fetch_supply_chain_news()
    print("\nFETCHING WEATHER DATA...")
    print("-"*30)

    fetch_port_weather()
    print("\nFETCHING SHIP DATA...")
    print("-"*30)

    asyncio.run(fetch_ship_data())
    print("\n"+"="*50)
    print("Pipeline Complete!")
    print("="*50)
run_pipeline()    


