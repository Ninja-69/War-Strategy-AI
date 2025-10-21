import wikipedia
import pandas as pd
import time
import os

print("WIKIPEDIA BATTLE SCRAPER - REAL")
print("Target: 15,000 battles")

os.makedirs('data/wikipedia', exist_ok=True)

search_terms = [
    "List of battles", "List of sieges", "World War I battles",
    "World War II battles", "Napoleonic battles", "Ancient battles",
    "Medieval battles", "American Civil War battles", "Vietnam War",
    "Korean War", "Iraq War", "Afghanistan War", "Crusades",
    "Roman battles", "Greek battles", "Persian battles",
    "Chinese battles", "Japanese battles", "Indian battles"
]

all_battles = []
seen = set()

print(f"Searching {len(search_terms)} categories...")

for idx, term in enumerate(search_terms, 1):
    try:
        print(f"  {idx}/{len(search_terms)} {term}...", end=" ")
        results = wikipedia.search(term, results=100)
        
        count = 0
        for result in results:
            if any(w in result.lower() for w in ['battle', 'siege', 'war', 'operation']):
                if result not in seen:
                    try:
                        page = wikipedia.page(result, auto_suggest=False)
                        all_battles.append({
                            'name': result,
                            'summary': page.summary[:500],
                            'url': page.url
                        })
                        seen.add(result)
                        count += 1
                        
                        if len(all_battles) % 100 == 0:
                            df = pd.DataFrame(all_battles)
                            df.to_csv('data/wikipedia/battles.csv', index=False)
                            print(f"
  Saved {len(all_battles)} battles")
                        
                    except:
                        continue
        
        print(f"{count} found (Total: {len(all_battles)})")
        time.sleep(0.5)
        
    except Exception as e:
        print(f"Error: {e}")
        continue

df = pd.DataFrame(all_battles)
df.to_csv('data/wikipedia/battles.csv', index=False)

print(f"
DONE! Scraped {len(all_battles)} real battles")
print(f"Saved to: data/wikipedia/battles.csv")
