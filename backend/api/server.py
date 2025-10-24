from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import chromadb
import requests
import os
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(project_root, '.env'))

app = Flask(__name__)
CORS(app)

vectordb_path = "/opt/war-room/War-Strategy-AI/data/vectordb/battle_vectordb"
chroma_client = chromadb.PersistentClient(path=vectordb_path)
collection = chroma_client.get_collection("battles")

print("="*50)
print("ARES PERFECTION v15.0")
print(f"Battles: {collection.count()}")
print("="*50)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "PERFECTION ONLINE", "battles": collection.count(), "version": "15.0"})

def ask_llama3_stream(messages):
    # Streaming with Ollama API (/api/chat, stream=true)
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": "llama3",
        "messages": messages,
        "stream": True
    }
    with requests.post(url, json=payload, stream=True) as response:
        response.raise_for_status()
        for line in response.iter_lines(decode_unicode=True):
            if line and line.strip().startswith("data:"):
                data = line.strip()[5:].strip()
                if data and data != "[DONE]":
                    try:
                        obj = __import__("json").loads(data)
                        content = obj.get("message", {}).get("content")
                        if content:
                            yield content
                    except Exception:
                        continue

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    results = collection.query(query_texts=[question], n_results=50)
    context_list = []
    for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
        battle_name = meta.get('name', 'Unknown')
        context_list.append(f"Battle: {battle_name}{doc}")
    context_text = "".join(context_list)
    prompt = f"ARES AI. CONTEXT: {context_text}SCENARIO: {question}Provide complete OPORD."

    messages = [{"role": "user", "content": prompt}]
    return Response(ask_llama3_stream(messages), mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
