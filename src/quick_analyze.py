import pandas as pd
import subprocess

df = pd.read_csv('data/battles/wikipedia_mega.csv')
print(f"Quick analyzing {len(df)} battles...")

analyzed = []

for idx, row in df.iterrows():
    # Ultra short prompt for speed
    prompt = f"{row['name']} {row['year']}: key lesson in 10 words"
    
    try:
        result = subprocess.run(['ollama', 'run', 'phi3:mini', prompt], 
                              capture_output=True, text=True, timeout=30)
        
        analyzed.append({
            'name': row['name'],
            'year': row['year'],
            'summary': row['summary'],
            'quick_insight': result.stdout.strip()[:200],
            'url': row['url']
        })
        
        if (idx + 1) % 50 == 0:
            print(f"{idx+1}/{len(df)}")
            pd.DataFrame(analyzed).to_csv('data/battles/quick_analyzed.csv', index=False)
        
    except:
        analyzed.append({
            'name': row['name'],
            'year': row['year'],
            'summary': row['summary'],
            'quick_insight': 'Historical battle',
            'url': row['url']
        })

pd.DataFrame(analyzed).to_csv('data/battles/quick_analyzed.csv', index=False)
print(f"Done! {len(analyzed)} battles")
