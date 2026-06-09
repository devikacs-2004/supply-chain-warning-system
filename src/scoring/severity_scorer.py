import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.nlp.disruption_detector import detect_disruptions, get_headlines

# Keywords weighted by severity
SEVERITY_WEIGHTS = {
    "disruption": 6,
    "shortage": 7,
    "halted": 8,
    "blocked": 8,
    "strike": 7,
    "flood": 9,
    "storm": 8,
    "congestion": 5,
    "delay": 4,
    "slowing": 3
}

def score_severity(disruption):
    score = 0
    for keyword in disruption["keywords"]:
        score += SEVERITY_WEIGHTS.get(keyword, 3)
    
    # Cap score at 10
    return min(score, 10)

def run_scorer():
    print("Fetching and analyzing headlines...")
    headlines = get_headlines()
    disruptions = detect_disruptions(headlines)
    
    print(f"\nScoring {len(disruptions)} disruptions...\n")
    print("=" * 50)
    
    for d in disruptions:
        score = score_severity(d)
        alert = "🚨 ALERT!" if score >= 7 else "⚠️  WARNING" if score >= 5 else "📝 LOW"
        
        print(f"{alert} — Score: {score}/10")
        print(f"Headline: {d['headline']}")
        print(f"Keywords: {d['keywords']}")
        print("-" * 50)

run_scorer()