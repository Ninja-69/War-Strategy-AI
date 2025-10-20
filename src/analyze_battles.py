import pandas as pd
import subprocess

print("LLM Battle Analyzer - Using Mistral")

df = pd.read_csv("data/battles/wikipedia_raw.csv")
print(f"Analyzing {len(df)} battles...")

analyzed = []

for idx, row in df.iterrows():
    battle_name = row["name"]
    battle_year = row["year"]
    battle_summary = row["summary"]
    
    prompt = f'''Analyze this battle and extract:

Battle: {battle_name}
Year: {battle_year}
Summary: {battle_summary}

Extract:
- Commander: (winning general name)
- Terrain: (type)
- Tactics: (3 words)
- Outcome: (who won)
- Lesson: (5 words max)

Be brief. One line per field.'''

    result = subprocess.run(["ollama", "run", "mistral:7b", prompt], 
                          capture_output=True, text=True, timeout=60)
    
    analysis = result.stdout
    
    analyzed.append({
        "name": battle_name,
        "year": battle_year,
        "summary": battle_summary,
        "analysis": analysis,
        "url": row["url"]
    })
    
    print(f"{idx+1}. {battle_name} analyzed")

df_analyzed = pd.DataFrame(analyzed)
df_analyzed.to_csv("data/battles/battles_analyzed.csv", index=False)
print(f"Done! Analyzed {len(analyzed)} battles!")
print("Saved to: data/battles/battles_analyzed.csv")
