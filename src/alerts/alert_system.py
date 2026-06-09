import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.forecasting.inventory_forecast import forecast_inventory
from src.scoring.severity_scorer import score_severity, get_headlines
from src.nlp.disruption_detector import detect_disruptions

SEVERITY_ALERT_THRESHOLD = 7
INVENTORY_ALERT_THRESHOLD = 500

def run_alert_system():
    print("=" * 60)
    print("🚨 SUPPLY CHAIN EARLY WARNING SYSTEM — ALERT ENGINE")
    print("=" * 60)
    
    # Get live disruptions
    print("\nFetching live news and detecting disruptions...")
    headlines = get_headlines()
    disruptions = detect_disruptions(headlines)
    
    alerts_fired = 0
    
    for d in disruptions:
        score = score_severity(d)
        
        if score >= SEVERITY_ALERT_THRESHOLD:
            print(f"\n🚨 HIGH SEVERITY DISRUPTION DETECTED!")
            print(f"Score: {score}/10")
            print(f"Headline: {d['headline']}")
            
            # Run inventory forecast
            forecast = forecast_inventory(score, d["headline"])
            
            # Check if inventory will drop below threshold
            future_forecast = forecast.tail(21)
            min_inventory = future_forecast["yhat"].min()
            min_date = future_forecast.loc[future_forecast["yhat"].idxmin(), "ds"]
            
            print(f"\n⚠️  INVENTORY ALERT:")
            print(f"Projected minimum inventory: {min_inventory:.0f} units")
            print(f"Expected on: {min_date.strftime('%Y-%m-%d')}")
            
            if min_inventory < INVENTORY_ALERT_THRESHOLD:
                print(f"🔴 CRITICAL: Inventory projected to drop below {INVENTORY_ALERT_THRESHOLD} units!")
                print(f"ACTION REQUIRED: Reorder stock immediately!")
            
            alerts_fired += 1
            print("-" * 60)
    
    if alerts_fired == 0:
        print("\n✅ No high severity disruptions detected today.")
    else:
        print(f"\n Total alerts fired: {alerts_fired}")

run_alert_system()