from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import chromadb
from groq import Groq
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Load .env from project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(project_root, '.env'))

app = Flask(__name__)
CORS(app)

# Initialize clients
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found! Create .env file in project root.")

groq_client = Groq(api_key=api_key)
vectordb_path = os.path.join(project_root, "data", "vectordb")
chroma_client = chromadb.PersistentClient(path=vectordb_path)
collection = chroma_client.get_collection("battles")

print("="*50)
print("ARES PERFECTION v15.0 - FINAL")
print(f"Battles loaded: {collection.count()}")
print(f"Vectordb path: {vectordb_path}")
print("="*50)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "PERFECTION ONLINE",
        "battles": collection.count(),
        "version": "15.0 FINAL"
    })

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    
    results = collection.query(query_texts=[question], n_results=50)
    
    context = []
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        context.append(f"Battle: {meta.get('name', 'Unknown')}
{doc}")
    context_text = "

".join(context)
    
    prompt = f"""ARES Military AI - Complete Strategic Analysis

HISTORICAL CONTEXT (50 battles):
{context_text}

SCENARIO: {question}

Provide complete OPORD with 30+ precedents, Lanchester analysis, GPS, logistics."""

    def generate():
        stream = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=8000
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    
    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
