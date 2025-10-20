import pandas as pd

print("Merging all battles...")

orig = pd.read_csv('data/battles/battles_complete.csv')
mega = pd.read_csv('data/battles/wikipedia_mega.csv')

print(f"Original: {len(orig)} battles")
print(f"Scraped: {len(mega)} battles")

mega_formatted = []
for idx, row in mega.iterrows():
    summary = row['summary'] if pd.notna(row['summary']) else 'Historic battle'
    mega_formatted.append({
        'name': row['name'],
        'year': row['year'],
        'general': 'Various',
        'location': 'See summary',
        'terrain': 'Various',
        'attacker_troops': 'Unknown',
        'defender_troops': 'Unknown',
        'attacker_tactics': 'See summary',
        'defender_tactics': 'See summary',
        'outcome': 'See summary',
        'key_lesson': 'Historic significance',
        'general_insight': summary[:200] if len(summary) > 200 else summary
    })

df_mega = pd.DataFrame(mega_formatted)
combined = pd.concat([orig, df_mega], ignore_index=True)
combined.to_csv('data/battles/battles_923.csv', index=False)

print(f"MERGED: {len(combined)} total battles!")
print(f"Saved to: data/battles/battles_923.csv")
