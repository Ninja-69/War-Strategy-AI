import wikipedia
import pandas as pd
import time
import re

battles = []
print("Wikipedia Battle Scraper v2")

# Specific battle names to search for
battle_names = [
    "Battle of Waterloo", "Battle of Gettysburg", "Battle of Marathon", 
    "Battle of Hastings", "Battle of Midway", "Battle of Tours",
    "Battle of Agincourt", "Battle of Leipzig", "Battle of Vienna",
    "Battle of Borodino", "Battle of Salamis", "Battle of Trafalgar",
    "Battle of Jutland", "Battle of Verdun", "Battle of the Somme",
    "Battle of Britain", "Battle of the Bulge", "Battle of Iwo Jima",
    "Battle of Kursk", "Battle of El Alamein", "Battle of Yorktown",
    "Battle of Actium", "Battle of Chalons", "Battle of Teutoburg",
    "Battle of Kadesh", "Battle of Sekigahara", "Battle of Red Cliffs",
    "Battle of Plassey", "Battle of Blenheim", "Battle of Saratoga",
    "Battle of Omdurman", "Battle of Tannenberg", "Battle of Poltava"
]

print(f"Scraping {len(battle_names)} famous battles...")

count = 0
for battle_name in battle_names:
    try:
        page = wikipedia.page(battle_name, auto_suggest=False)
        summary = page.summary[:500]
        
        year_match = re.search(r"\b(\d{1,4})\s*(BC|AD|CE)?\b", summary)
        year = year_match.group(0) if year_match else "Unknown"
        
        battles.append({
            "name": battle_name.replace("Battle of ", ""),
            "year": year,
            "summary": summary,
            "url": page.url
        })
        
        count += 1
        print(f"{count}. {battle_name} ({year})")
        time.sleep(0.3)
        
    except Exception as e:
        print(f"Skipped: {battle_name}")
        continue

df = pd.DataFrame(battles)
df.to_csv("data/battles/wikipedia_raw.csv", index=False)
print(f"Scraped {len(battles)} battles! Saved to wikipedia_raw.csv")
print("Next: Use LLM to extract tactics, commanders, and outcomes!")
