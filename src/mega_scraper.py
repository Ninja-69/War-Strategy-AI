import wikipedia
import pandas as pd
import time

battles = []
print("MEGA BATTLE SCRAPER - Target: 1000+ battles")
print("")

search_terms = [
    "Battle of", "Siege of", "War", "Campaign",
    "World War I battles", "World War II battles", 
    "Napoleonic battles", "Ancient battles", "Medieval battles",
    "American Civil War battles", "Roman battles", "Greek battles",
    "Mongol battles", "Ottoman battles", "Persian battles",
    "Chinese battles", "Japanese battles", "Indian battles",
    "African battles", "South American battles",
    "Vietnam War battles", "Korean War battles",
    "Crusades battles", "French Revolutionary battles",
    "Byzantine battles", "Viking battles", "Arab battles"
]

all_battle_names = set()

print("Phase 1: Searching Wikipedia...")
print("")

for term in search_terms:
    try:
        results = wikipedia.search(term, results=50)
        for r in results:
            if any(word in r.lower() for word in ['battle', 'siege', 'war', 'campaign']):
                all_battle_names.add(r)
        print(f"Searched '{term}': {len(all_battle_names)} unique pages")
        time.sleep(0.5)
    except:
        continue

print("")
print(f"Phase 2: Extracting {len(all_battle_names)} battles...")
print("")

count = 0
for battle_name in list(all_battle_names):
    try:
        page = wikipedia.page(battle_name, auto_suggest=False)
        summary = page.summary[:500]
        
        import re
        year_match = re.search(r'\b(d{1,4})s*(BC|AD|CE)?\b', battle_name + ' ' + summary)
        year = year_match.group(0) if year_match else 'Unknown'
        
        battles.append({
            'name': battle_name.replace('Battle of ', '').replace('Siege of ', ''),
            'year': year,
            'summary': summary,
            'url': page.url
        })
        
        count += 1
        if count % 50 == 0:
            print(f"Progress: {count} battles scraped...")
        
        time.sleep(0.3)
        
    except:
        continue

df = pd.DataFrame(battles)
df.to_csv('data/battles/wikipedia_mega.csv', index=False)
print("")
print(f"SCRAPED {len(battles)} BATTLES!")
print("Saved to: data/battles/wikipedia_mega.csv")
