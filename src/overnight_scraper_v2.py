import wikipedia
import pandas as pd
import time
import os
from datetime import datetime

print("=" * 70)
print("OVERNIGHT SCRAPER v2 - FIXED")
print("=" * 70)

os.makedirs("data/overnight", exist_ok=True)

# Load existing data
existing = []
if os.path.exists("data/overnight/wikipedia_battles.csv"):
    try:
        df = pd.read_csv("data/overnight/wikipedia_battles.csv")
        existing = df["name"].tolist()
        print(f"Resuming... Already have {len(existing)} battles")
    except:
        pass

battles = existing.copy() if existing else []
seen = set(existing)

search_terms = [
    "World War II battles", "World War I battles", "Napoleonic battles",
    "Ancient Roman battles", "Medieval battles", "American Civil War",
    "Vietnam War battles", "Korean War battles", "Crusades battles",
    "Greek battles", "Persian battles", "Chinese battles"
]

print(f"Scraping {len(search_terms)} categories...")

for idx, term in enumerate(search_terms, 1):
    try:
        print(f"{idx}/{len(search_terms)} {term}...")
        results = wikipedia.search(term, results=50)
        
        for result in results:
            if result in seen:
                continue
                
            try:
                page = wikipedia.page(result, auto_suggest=False)
                battles.append({
                    "name": result,
                    "summary": page.summary[:1000],
                    "url": page.url,
                    "source": "Wikipedia"
                })
                seen.add(result)
                
                if len(battles) % 50 == 0:
                    df = pd.DataFrame(battles)
                    df.to_csv("data/overnight/wikipedia_battles.csv", index=False)
                    print(f"  Saved {len(battles)} total")
                
                time.sleep(2)
                
            except:
                continue
        
        time.sleep(5)
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
        continue

df = pd.DataFrame(battles)
df.to_csv("data/overnight/wikipedia_battles.csv", index=False)
print(f"DONE! {len(battles)} battles total")
