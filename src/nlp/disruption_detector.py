import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.ingestion.fetch_news import fetch_supply_chain_news

DISRUPTION_KEYWORDS = [
    "disruption", "delay", "shortage", "congestion",
    "strike", "flood", "storm", "blocked", "halted", "slowing"
]

def detect_disruptions(headlines):
    disruptions = []
    
    for headline in headlines:
        headline_lower = headline.lower()
        matched_keywords = []
        
        for keyword in DISRUPTION_KEYWORDS:
            if keyword in headline_lower:
                matched_keywords.append(keyword)
        
        if matched_keywords:
            disruptions.append({
                "headline": headline,
                "keywords": matched_keywords
            })
    
    return disruptions

def get_headlines():
    import requests
    from dotenv import load_dotenv
    load_dotenv()
    
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "supply chain disruption OR port congestion OR shipping delay",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return [article["title"] for article in data["articles"]]

if __name__ == "__main__":
    print("Fetching headlines...")
    headlines = get_headlines()
    
    print(f"Total headlines fetched: {len(headlines)}")
    print("\nDetecting disruptions...")
    disruptions = detect_disruptions(headlines)
    
    print(f"Disruptions detected: {len(disruptions)}")
    print("\n--- DISRUPTED HEADLINES ---")
    for d in disruptions:
        print(f"Headline: {d['headline']}")
        print(f"Keywords: {d['keywords']}")
        print("---")