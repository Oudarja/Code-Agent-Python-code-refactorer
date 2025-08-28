# src/rag/embedder.py

import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import faiss
import pickle
from sentence_transformers import SentenceTransformer

def embed_and_save(chunks, metadata):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    faiss.write_index(index,"repo_index.faiss")

    with open("metadata.pkl", "wb") as f:
        pickle.dump(metadata, f)

    print("✅ Embeddings & metadata saved.")
