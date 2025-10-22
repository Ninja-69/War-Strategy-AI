from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import chromadb
from groq import Groq

app = Flask(__name__)
CORS(app)

groq_client = Groq(api_key="YOUR_API_KEY_HERE")
chroma_client = chromadb.PersistentClient(path="./battle_vectordb")
collection = chroma_client.get_collection("battles")

PROMPT = """You are ARES - Supreme Military AI. Provide: GPS coordinates, 25+ historical battles, Lanchester analysis, logistics breakdown, cyber targets, hour-by-hour timeline, casualty projections, deception ops, probability analysis."""

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    res = collection.query(query_texts=[question], n_results=50)
    ctx = "DATABASE: " + str(collection.count()) + " battles"
    if res and res["documents"]:
        for i, doc in enumerate(res["documents"][0][:30]):
            ctx += "[BATTLE " + str(i+1) + "]" + doc[:2000] + ""
    def generate():
        yield "[ARES ANALYSIS]"
        stream = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": PROMPT}, {"role": "user", "content": ctx + "MISSION: " + question}],
            temperature=0.95,
            max_tokens=8000,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    return Response(generate(), mimetype="text/plain")

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ONLINE", "battles": collection.count()})

if __name__ == "__main__":
    print("ARES v13.0 RUNNING")
    app.run(host="0.0.0.0", port=5000)
