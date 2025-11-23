#!/usr/bin/env python3
"""
Basic FAISS microservice using FastAPI.
Provides endpoints for adding vectors and searching similar vectors.
"""

import numpy as np
from fastapi import FastAPI, HTTPException
from typing import List, Tuple
import faiss
from models import *

app = FastAPI(title="FAISS Microservice", version="1.0.0")

# In-memory FAISS index (basic implementation)
# Using IndexFlatIP for inner product (cosine similarity with normalized vectors)
dimension = 384  # Embedding dimension for sentence-transformers
index = faiss.IndexFlatIP(dimension)
id_to_vector = {}  # Map IDs to vectors
vector_to_id = {}  # Map vector indices to IDs
next_id = 0



@app.post("/add_vector")
async def add_vector(data: VectorData):
    """Add a vector to the FAISS index."""
    global next_id

    vector = np.array(data.vector, dtype=np.float32)

    if len(vector) != dimension:
        raise HTTPException(status_code=400, detail=f"Vector dimension must be {dimension}")

    # Normalize vector for cosine similarity
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm

    # Add to FAISS index
    index.add(vector.reshape(1, -1))

    # Store mapping
    id_to_vector[data.id] = vector
    vector_to_id[next_id] = data.id
    next_id += 1

    return {"message": f"Vector with ID '{data.id}' added successfully"}

@app.post("/search", response_model=List[SearchResult])
async def search_similar(query: SearchQuery):
    """Search for similar vectors in the index."""
    if index.ntotal == 0:
        return []

    vector = np.array(query.vector, dtype=np.float32)

    if len(vector) != dimension:
        raise HTTPException(status_code=400, detail=f"Vector dimension must be {dimension}")

    # Normalize query vector
    norm = np.linalg.norm(vector)
    if norm > 0:
        vector = vector / norm

    # Search
    D, I = index.search(vector.reshape(1, -1), min(query.k, index.ntotal))

    results = []
    for score, idx in zip(D[0], I[0]):
        if idx != -1:  # Valid result
            result_id = vector_to_id.get(idx, "unknown")
            results.append(SearchResult(id=result_id, score=float(score)))

    return results

@app.get("/status")
async def get_status():
    """Get index status."""
    return {
        "total_vectors": index.ntotal,
        "dimension": dimension,
        "index_type": "IndexFlatIP"
    }

@app.get("/get_all")
async def get_all_vectors():
    """Get all vectors in the index."""
    return {"vectors": [{"id": vector_to_id[i], "vector": id_to_vector[vector_to_id[i]].tolist()} for i in range(next_id) if i in vector_to_id]}

@app.get("/get_all_id")
async def get_all_ids():
    return {"vectors": [{"id": vector_to_id[i]} for i in range(next_id) if i in vector_to_id]}
   

@app.delete("/clear")
async def clear_index():
    """Clear all vectors from the index."""
    global index, id_to_vector, vector_to_id, next_id
    index = faiss.IndexFlatIP(dimension)
    id_to_vector = {}
    vector_to_id = {}
    next_id = 0
    return {"message": "Index cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)