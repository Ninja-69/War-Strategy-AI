import pandas as pd
from sentence_transformers import SentenceTransformer
import chromadb

print("Loading battles...")
df = pd.read_csv('data/battles/battles_v1.csv')

print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

print("Creating vector database...")
client = chromadb.PersistentClient(path="data/embeddings")
collection = client.get_or_create_collection("battles")

print("Generating embeddings...")
for idx, row in df.iterrows():
    text = f"{row['name']} ({row['year']}): {row['terrain']} terrain. {row['attacker_troops']} vs {row['defender_troops']}. Tactics: {row['attacker_tactics']} vs {row['defender_tactics']}. {row['outcome']}. Lesson: {row['key_lesson']}"
    
    embedding = model.encode(text).tolist()
    collection.add(embeddings=[embedding], documents=[text], metadatas={"name": row['name']}, ids=[f"battle_{idx}"])
    print(f"  Embedded: {row['name']}")

print(f"Done! Embedded {len(df)} battles!")
