import asyncio
import websockets
import json
import os
from dotenv import load_dotenv

load_dotenv()
AISSTREAM_API_KEY=os.getenv("AISSTREAM_API_KEY")
async def fetch_ship_data():
    url="wss://stream.aisstream.io/v0/stream"
    subscribe_message={
        "APIKey":AISSTREAM_API_KEY,
        "BoundingBoxes":[
            #Major shipping lanes-Singapore strait
            [[1.0, 103.0], [1.5, 104.5]],
        ],
        "FilterMessageTypes": ["PositionReport"]
    }
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps(subscribe_message))
        print("Connected to AISStream-receiving ship data...")

        count=0
        async for message in websocket:
            data=json.loads(message)
            if "Message" in data:
                mmsi= data.get("MetaData", {}).get("MMSI","Unknown")
                ship_name=data.get("MetaData", {}).get("ShipName","Unknown")
                lat=data.get("MetaData", {}).get("Latitude","Unknown")
                lon=data.get("MetaData", {}).get("Longitude","Unknown")
                print(f"Ship: {ship_name.strip()}")
                print(f"MMSI:{mmsi}")
                print(f"Location:{lat},{lon}")
                print("---")
                count +=1
                if count>=5: #stop after 5 ship
                    break
asyncio.run(fetch_ship_data())