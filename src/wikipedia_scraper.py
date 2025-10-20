import wikipedia
import pandas as pd
import time

battles = []

print('Starting Wikipedia Battle Scraper...
')

# List of major battle pages to scrape
battle_searches = [
    'List of battles',
    'List of battles 1801-1900', 
    'List of battles 1901-2000',
    'List of battles (alphabetical)',
    'Ancient warfare',
    'Medieval warfare',
    'Napoleonic Wars battles',
    'World War II battles',
    'Ancient Greek battles',
    'Roman battles'
]

print('Searching Wikipedia for battle lists...
')

# Get all battle links
all_battles = set()
for search in battle_searches:
    try:
        page = wikipedia.search(search, results=1)
        if page:
            print(f'  Found: {page[0]}')
            all_battles.add(page[0])
    except:
        pass
    time.sleep(0.5)

print(f'
Found {len(all_battles)} battle pages. Extracting details...
')

# Extract battle details
count = 0
for battle_name in list(all_battles)[:100]:
    try:
        page = wikipedia.page(battle_name, auto_suggest=False)
        summary = page.summary[:500]
        
        import re
        year_match = re.search(r'\b(d{1,4})s*(BC|AD|CE)?\b', battle_name + ' ' + summary)
        year = year_match.group(0) if year_match else 'Unknown'
        
        battles.append({
            'name': battle_name,
            'year': year,
            'summary': summary,
            'url': page.url
        })
        
        count += 1
        print(f'  {count}. {battle_name} ({year})')
        time.sleep(0.3)
        
    except Exception as e:
        print(f'  Skipped: {battle_name}')
        continue

print(f'
Scraped {len(battles)} battles!')

df = pd.DataFrame(battles)
df.to_csv('data/battles/wikipedia_battles_raw.csv', index=False)
print(f'Saved to: data/battles/wikipedia_battles_raw.csv')
print(f'
Next: Process this data with LLM to extract tactics and generals!')
