import chromadb
from chromadb.config import Settings
import json

print("Loading battles dataset...")
battles = []
with open("training_data.jsonl", "r") as f:
    for line in f:
        battles.append(json.loads(line))

print(f"Loaded {len(battles)} battles")

print("Initializing ChromaDB...")
client = chromadb.PersistentClient(path="./battle_vectordb")

try:
    client.delete_collection("battles")
except:
    pass

collection = client.create_collection(
    name="battles",
    metadata={"description": "100K+ historical battles"}
)

print("Storing battles in vector database...")
batch_size = 100
for i in range(0, len(battles), batch_size):
    batch = battles[i:i+batch_size]
    
    documents = []
    metadatas = []
    ids = []
    
    for idx, battle in enumerate(batch):
        instruction = battle.get("instruction", "")
        response = battle.get("response", "")
        doc = instruction + " " + response
        documents.append(doc)
        metadatas.append({
            "instruction": instruction,
            "response": response[:500]
        })
        ids.append(f"battle_{i+idx}")
    
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    if (i // batch_size) % 10 == 0:
        print(f"Progress: {i}/{len(battles)} battles indexed")

print("Vector database created successfully!")
print(f"Total battles indexed: {collection.count()}")
