import pandas as pd
import numpy as np
from prophet import Prophet
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def generate_inventory_data(severity_score, days=30):
    """
    Simulate historical inventory levels affected by a disruption.
    Higher severity = steeper drop.
    """
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)
    baseline = 1000  # baseline inventory units
    
    inventory = []
    for i, date in enumerate(dates):
        # Disruption starts at day 20
        if i < 20:
            level = baseline + np.random.normal(0, 20)
        else:
            # Drop based on severity
            drop = (severity_score / 10) * 30 * (i - 19)
            level = baseline - drop + np.random.normal(0, 20)
        
        inventory.append(max(level, 0))  # inventory can't go negative
    
    df = pd.DataFrame({
        "ds": dates,
        "y": inventory
    })
    return df

def forecast_inventory(severity_score, headline):
    print(f"\nForecasting inventory impact for:")
    print(f"'{headline}'")
    print(f"Severity Score: {severity_score}/10")
    
    # Generate historical data
    df = generate_inventory_data(severity_score)
    
    # Train Prophet model
    model = Prophet(daily_seasonality=False, weekly_seasonality=True)
    model.fit(df)
    
    # Forecast 21 days ahead (3 weeks)
    future = model.make_future_dataframe(periods=21)
    forecast = model.predict(future)
    
    # Show forecast for next 3 weeks
    future_forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(21)
    
    print(f"\n📈 3-Week Inventory Forecast:")
    print("-" * 50)
    for _, row in future_forecast.iterrows():
        print(f"Date: {row['ds'].strftime('%Y-%m-%d')} | "
              f"Predicted: {row['yhat']:.0f} units | "
              f"Range: {row['yhat_lower']:.0f} - {row['yhat_upper']:.0f}")
    
    return forecast

if __name__ == "__main__":
    forecast_inventory(7, "Frozen price caps cause shortage of chemotherapy drugs in India")