import pandas as pd
import subprocess
import sys

print("MEGA BATTLE ANALYZER - Using Mistral LLM")
print("")

df = pd.read_csv('data/battles/wikipedia_mega.csv')
total = len(df)
print(f"Analyzing ALL {total} battles...")
print(f"Estimated time: {total * 0.5 / 60:.1f} hours")
print("")

analyzed = []
count = 0

for idx, row in df.iterrows():
    prompt = f"""Analyze: {row['name']} ({row['year']})
Summary: {row['summary']}

Extract in one line each:
Commander: 
Terrain: 
Tactics: 
Outcome: 
Lesson:"""

    try:
        result = subprocess.run(['ollama', 'run', 'mistral:7b', prompt], 
                              capture_output=True, text=True, timeout=60)
        
        analyzed.append({
            'name': row['name'],
            'year': row['year'],
            'summary': row['summary'],
            'analysis': result.stdout,
            'url': row['url']
        })
        
        count += 1
        if count % 10 == 0:
            print(f"Progress: {count}/{total} analyzed")
            pd.DataFrame(analyzed).to_csv('data/battles/mega_analyzed_temp.csv', index=False)
        
    except Exception as e:
        print(f"Skipped: {row['name']} - {e}")
        continue

df_final = pd.DataFrame(analyzed)
df_final.to_csv('data/battles/mega_analyzed.csv', index=False)
print("")
print(f"DONE! Analyzed {len(analyzed)} battles")
print("Saved to: data/battles/mega_analyzed.csv")
