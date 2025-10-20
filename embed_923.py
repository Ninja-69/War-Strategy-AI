import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

df = pd.read_csv('data/battles/battles_923.csv')
print(f"Embedding {len(df)} battles...")

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path='data/embeddings')

try:
    client.delete_collection('battles')
    print("Deleted old collection")
except:
    pass

collection = client.create_collection('battles')

for idx, row in df.iterrows():
    text = f"{row['name']} {row['year']} {row['general']} {row['terrain']} {row['general_insight']}"
    emb = model.encode(text).tolist()
    collection.add(
        embeddings=[emb], 
        documents=[text], 
        metadatas={'name': row['name'], 'general': row['general']}, 
        ids=[f'b{idx}']
    )
    if (idx + 1) % 100 == 0:
        print(f"  {idx+1}/{len(df)} embedded...")

print(f"DONE! All {len(df)} battles embedded!")
