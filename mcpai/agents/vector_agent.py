
import os
import json
from redis_pubsub import subscribe
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

VECTOR_BASE = "vector_store"
MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

os.makedirs(VECTOR_BASE, exist_ok=True)

def update_vector_store(msg):
    zone = msg.get("zone", "default")
    value = str(msg["value"])
    vector_path = os.path.join(VECTOR_BASE, f"{zone}.index")
    text_path = os.path.join(VECTOR_BASE, f"{zone}.jsonl")

    embedding = MODEL.encode([value])[0].astype(np.float32)

    # Save vector
    if os.path.exists(vector_path):
        index = faiss.read_index(vector_path)
    else:
        index = faiss.IndexFlatL2(embedding.shape[0])

    index.add(np.array([embedding]))
    faiss.write_index(index, vector_path)

    with open(text_path, "a") as f:
        f.write(json.dumps({"text": value}) + "\n")

    print(f"[VectorAgent] Updated vector store for zone: {zone}")

def run_vector_agent():
    subscribe("filter/passed", update_vector_store)
