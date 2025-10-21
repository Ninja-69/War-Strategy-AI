import pandas as pd
import json

df = pd.read_csv('military_battles_dataset_100k.csv')
df_clean = df[(df['battle'].notna()) & (df['analysis'].notna()) & (df['outcome'].notna())].copy()

training_data = []
for idx, row in df_clean.iterrows():
    training_data.append({
        "instruction": "Analyze the Battle of " + str(row['battle']),
        "response": "Battle: " + str(row['battle']) + "
Analysis: " + str(row['analysis']) + "
Outcome: " + str(row['outcome'])
    })

with open('training_data.jsonl', 'w') as f:
    for item in training_data:
        f.write(json.dumps(item))
        f.write('
')

pd.DataFrame(training_data).to_csv('training_data.csv', index=False)
print("Created " + str(len(training_data)) + " examples")
