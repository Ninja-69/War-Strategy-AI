from sentence_transformers import SentenceTransformer
import chromadb
import subprocess

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="data/embeddings")
collection = client.get_collection("battles")

def query_agent(name, model_name, prompt):
    print("" + "="*70)
    print("AGENT:", name.upper())
    print("="*70 + "")
    result = subprocess.run(['ollama', 'run', model_name, prompt], capture_output=True, text=True, timeout=180)
    print(result.stdout)
    return result.stdout

def analyze(scenario):
    print("" + "#"*70)
    print("SCENARIO:", scenario)
    print("#"*70 + "")
    
    print("Retrieving historical battles...")
    emb = model.encode(scenario).tolist()
    results = collection.query(query_embeddings=[emb], n_results=2)
    battles = results['documents'][0]
    
    print("Found", len(battles), "relevant battles")
    
    query_agent("Terrain Analyst", "phi3:mini", "Terrain analysis: " + scenario + ". Brief 3 sentences.")
    
    query_agent("Military Historian", "mistral:7b", "Relevant battles: " + battles[0] + ". " + battles[1] + ". How do they relate to: " + scenario + "? Brief 4 sentences.")
    
    query_agent("Chief Tactician", "llama3.1:8b", "Scenario: " + scenario + ". Give 3 strategy options. Be concise.")
    
    query_agent("Logistics Officer", "qwen2.5:7b", "Supply needs for: " + scenario + ". Brief 3 sentences.")
    
    print("" + "="*70)
    print("WAR ROOM COMPLETE")
    print("="*70)

print("MULTI-AGENT WAR ROOM")
scenarios = [
    "Defend mountain pass with 5000 troops vs 20000 with cavalry",
    "Amphibious assault on fortified beach",
    "Urban winter combat outnumbered 2 to 1"
]

for i, s in enumerate(scenarios, 1):
    print(str(i) + ".", s)

choice = input("Select 1-3: ")
sc = scenarios[int(choice)-1]
analyze(sc)
