import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

print('Loading battles...')
df = pd.read_csv('data/battles/battles_v2.csv')
print(f'Found {len(df)} battles')

print('Loading model...')
model = SentenceTransformer('all-MiniLM-L6-v2')

print('Creating vector database...')
client = chromadb.PersistentClient(path='data/embeddings')
try:
    client.delete_collection('battles')
    print('Deleted old collection')
except:
    pass
collection = client.create_collection('battles')

print('Embedding battles:')
for idx, row in df.iterrows():
    text = f"{row['name']} ({row['year']}) by {row['general']}: {row['terrain']} terrain. {row['attacker_troops']} vs {row['defender_troops']}. Tactics: {row['attacker_tactics']} vs {row['defender_tactics']}. {row['outcome']}. Lesson: {row['key_lesson']}. Insight: {row['general_insight']}"
    
    embedding = model.encode(text).tolist()
    collection.add(embeddings=[embedding], documents=[text], metadatas={'name': row['name'], 'general': row['general']}, ids=[f'battle_{idx}'])
    print(f'  {idx+1}. {row["name"]} - {row["general"]}')

print(f'Done! Embedded {len(df)} battles!')
