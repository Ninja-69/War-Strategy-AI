from sentence_transformers import SentenceTransformer
import chromadb
import subprocess

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path='data/embeddings')
collection = client.get_collection('battles')

def query_agent(name, model_name, prompt):
    print('' + '='*70)
    print('AGENT:', name.upper())
    print('='*70 + '')
    result = subprocess.run(['ollama', 'run', model_name, prompt], capture_output=True, text=True, timeout=180)
    print(result.stdout)
    return result.stdout

def analyze(scenario):
    print('' + '#'*70)
    print('SCENARIO:', scenario)
    print('#'*70 + '')
    
    print('Searching historical battles...')
    emb = model.encode(scenario).tolist()
    results = collection.query(query_embeddings=[emb], n_results=3)
    battles = results['documents'][0]
    generals = results['metadatas'][0]
    
    print('Found 3 relevant battles:')
    for i, (battle, meta) in enumerate(zip(battles, generals), 1):
        print(f'  {i}. {meta["name"]} - {meta["general"]}')
    
    context = ''.join([f'{i+1}. {doc}' for i, doc in enumerate(battles)])
    
    query_agent('Terrain Analyst', 'phi3:mini', f'Analyze terrain for: {scenario}. Be concise, 3 sentences.')
    
    hist = query_agent('Historical Strategist - Channeling ' + generals[0]['general'], 'mistral:7b', 
                       f'You are {generals[0]["general"]}. Relevant battles: {battles[0]}. {battles[1]}. Given scenario: {scenario}. What would {generals[0]["general"]} do? Think like him. 4 sentences.')
    
    query_agent('Chief Tactician', 'llama3.1:8b', 
                f'Scenario: {scenario}. Historical context: {hist[:500]}. Provide 3 strategic options with pros and cons. Be specific.')
    
    query_agent('Logistics Commander', 'qwen2.5:7b', 
                f'Supply and logistics assessment for: {scenario}. Consider terrain, troop movements, supply lines. 3 sentences.')
    
    print('' + '='*70)
    print('WAR ROOM ANALYSIS COMPLETE')
    print('='*70)

print('MULTI-AGENT WAR ROOM v2.0 - WITH GENERAL INSIGHTS')
scenarios = [
    'Defend mountain pass with 5000 troops vs 20000 with cavalry',
    'Amphibious assault on fortified beach with air cover',
    'Urban winter combat outnumbered 2 to 1 defending city',
    'Desert warfare with mobile armor vs entrenched enemy',
    'River crossing under enemy artillery fire'
]

for i, s in enumerate(scenarios, 1):
    print(f'{i}. {s}')

choice = input('Select 1-5 or enter custom scenario: ')
if choice in ['1','2','3','4','5']:
    sc = scenarios[int(choice)-1]
else:
    sc = choice
    
analyze(sc)
