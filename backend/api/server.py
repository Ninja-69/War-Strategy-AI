from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import chromadb
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.PersistentClient(path="../../data/vectordb")
collection = chroma_client.get_collection("battles")

# ... rest of your code ...
