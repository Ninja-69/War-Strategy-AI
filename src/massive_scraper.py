import wikipedia
import pandas as pd
import time
import os
from datetime import datetime

print("=" * 70)
print("MASSIVE WIKIPEDIA SCRAPER - 50K TARGET")
print("Started:", datetime.now())
print("=" * 70)

os.makedirs("data/massive", exist_ok=True)

battles = []
seen = set()

# MASSIVE search term list
search_terms = [
    "World War II battles", "World War I battles", "Napoleonic Wars",
    "American Civil War battles", "Vietnam War", "Korean War",
    "Ancient Roman battles", "Greek Persian Wars", "Medieval battles",
    "Crusades", "Ottoman Empire battles", "Byzantine battles",
    "Chinese history wars", "Japanese battles", "Indian battles",
    "American Revolutionary War", "Spanish Civil War", "Iraq War",
    "Afghanistan War", "Gulf War", "Balkan Wars", "Russo-Japanese War",
    "Franco-Prussian War", "Crimean War", "Boer Wars", "Hundred Years War",
    "Thirty Years War", "Seven Years War", "War of 1812",
    "Mexican-American War", "Spanish-American War", "Punic Wars",
    "Alexander the Great campaigns", "Genghis Khan conquests",
    "Napoleon battles", "Julius Caesar battles", "Hannibal battles",
    "Mongol invasions", "Viking raids", "Roman civil wars",
    "English Civil War", "Wars of the Roses", "Jacobite rising",
    "Israeli-Arab conflicts", "Indo-Pakistani wars", "Sino-Japanese wars",
    "Russian Revolution", "Chinese Civil War", "Finnish Winter War",
    "Polish-Soviet War", "Turkish War of Independence",
    "List of battles 18th century", "List of battles 19th century",
    "List of battles 20th century", "List of sieges in history",
    "Naval battles in history", "Air battles World War 2",
    "Tank battles", "Amphibious operations", "Guerrilla warfare"
]

print(f"Searching {len(search_terms)} categories...")
print(f"Target: 50,000 battles")

for idx, term in enumerate(search_terms, 1):
    try:
        print(f"{idx}/{len(search_terms)} {term}...", end=" ", flush=True)
        results = wikipedia.search(term, results=100)
        
        count = 0
        for result in results:
            if result in seen:
                continue
            
            try:
                page = wikipedia.page(result, auto_suggest=False)
                battles.append({
                    "title": result,
                    "summary": page.summary[:2000],
                    "url": page.url,
                    "category": term
                })
                seen.add(result)
                count += 1
                
                if len(battles) % 100 == 0:
                    df = pd.DataFrame(battles)
                    df.to_csv("data/massive/wikipedia_battles.csv", index=False)
                    print(f"💾 Saved {len(battles)} battles")
                    print(f"{idx}/{len(search_terms)} {term}...", end=" ", flush=True)
                
                time.sleep(1.5)
                
            except:
                continue
        
        print(f"✅ +{count} (Total: {len(battles)})")
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ {e}")
        time.sleep(5)

df = pd.DataFrame(battles)
df.to_csv("data/massive/wikipedia_battles.csv", index=False)

print("" + "=" * 70)
print(f"COMPLETE! Total: {len(battles)} battles")
print(f"Finished: {datetime.now()}")
print("=" * 70)
