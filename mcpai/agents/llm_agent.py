
import os
import json
from redis_pubsub import subscribe, publish
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

VECTOR_BASE = "vector_store"
MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def query_llm(msg):
    question = msg.get("question")
    zone = msg.get("zone", "default")

    vector_path = os.path.join(VECTOR_BASE, f"{zone}.index")
    text_path = os.path.join(VECTOR_BASE, f"{zone}.jsonl")

    if not os.path.exists(vector_path):
        publish("query/response", {"answer": "No vector data available for zone."})
        return

    query_vec = MODEL.encode([question]).astype(np.float32)
    index = faiss.read_index(vector_path)
    D, I = index.search(query_vec, k=3)

    with open(text_path, "r") as f:
        texts = [json.loads(line)["text"] for line in f.readlines()]

    context = [texts[i] for i in I[0] if i < len(texts)]
    answer = f"Answer based on context: {context}"
    publish("query/response", {"answer": answer})

def run_llm_agent():
    subscribe("query/request", query_llm)
