import pandas as pd
import wikipedia
import time
from datetime import datetime

print("="*70)
print("ENHANCING WIKIDATA WITH WIKIPEDIA SUMMARIES")
print("Started:", datetime.now())
print("="*70)

# Load Wikidata battles
df = pd.read_csv("data/wikidata_battles.csv")
print(f"Loaded {len(df)} battles from Wikidata")

# Load existing scraper data to avoid duplicates
existing = set()
try:
    scraper_df = pd.read_csv("data/massive/wikipedia_battles.csv")
    existing = set(scraper_df["title"].tolist())
    print(f"Found {len(existing)} existing battles from scraper")
except:
    print("No scraper data yet")

enhanced_battles = []
failed = 0

for idx, row in df.iterrows():
    battle_name = row["battleLabel"]
    
    # Skip if already scraped
    if battle_name in existing:
        continue
    
    try:
        print(f"{idx+1}/{len(df)} {battle_name}...", end=" ", flush=True)
        
        # Get Wikipedia page
        page = wikipedia.page(battle_name, auto_suggest=False)
        
        enhanced_battles.append({
            "title": battle_name,
            "summary": page.summary[:2000],
            "url": page.url,
            "date": row.get("date", ""),
            "location": row.get("location", ""),
            "source": "Wikidata+Wikipedia"
        })
        
        print("✅")
        
        # Save every 100
        if len(enhanced_battles) % 100 == 0:
            temp_df = pd.DataFrame(enhanced_battles)
            temp_df.to_csv("data/enhanced_battles.csv", index=False)
            print(f"💾 Saved {len(enhanced_battles)} enhanced battles")
        
        time.sleep(2)  # Be nice to Wikipedia
        
    except Exception as e:
        print(f"❌ {e}")
        failed += 1
        if failed > 50:
            time.sleep(10)  # Cool down if too many failures
            failed = 0
        continue

# Final save
df_final = pd.DataFrame(enhanced_battles)
df_final.to_csv("data/enhanced_battles.csv", index=False)

print("" + "="*70)
print(f"DONE! Enhanced {len(enhanced_battles)} battles")
print(f"Saved to: data/enhanced_battles.csv")
print("="*70)
