import requests
import os
from dotenv import load_dotenv
load_dotenv()
NEWS_API_KEY=os.getenv("NEWS_API_KEY")

def fetch_supply_chain_news():
    url="https://newsapi.org/v2/everything"
    params={
        "q":"supply chain instruction OR port congestion OR shipping delay",
        "language":"en",
        "sortBy":"publishedAt",
        "pageSize":10,
        "apiKey":NEWS_API_KEY
    }
    response=requests.get(url,params=params)
    data= response.json()
    for article in data["articles"]:
        print(article["title"])
        print(article["publishedAt"])
        print("---")
fetch_supply_chain_news()