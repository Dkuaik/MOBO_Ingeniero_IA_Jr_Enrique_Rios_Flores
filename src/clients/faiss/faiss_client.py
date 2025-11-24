import requests
from typing import List, Dict, Any
import numpy as np
import os
import sys
sys.path.insert(0, 'src')
from sentence_transformers import SentenceTransformer
from clients.mongodb.mongodb_client import MongoDBClient
from services.database.models.document_model import Document
from config.settings import MONGODB_URI, DATABASE_NAME, RAG_DATA_PATH, ROLE_MAPPING

# Configuración de los embeddings
MAX_CHUNK_SIZE = 1000  # Numero máximo de caracteres por chunk
OVERLAP_SIZE = 200     # Numero de caracteres de overlap

def split_text_with_overlap(text: str, max_chunk_size: int, overlap_size: int):
    """Split text into chunks with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chunk_size
        if end < len(text):
            chunk = text[start:end]
        else:
            chunk = text[start:]
        chunks.append(chunk)
        start = end - overlap_size
        if start >= len(text):
            break
    return chunks

# Definición del cliente con le cual nos vamos a comunicar con el servicio de FAISS
class FAISSClient:
    """FAISS client for vector similarity search operations."""

    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def add_vector(self, vector_id: str, vector: List[float], metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Add a vector to the FAISS index."""
        url = f"{self.base_url}/add_vector"
        data = {
            "id": vector_id,
            "vector": vector,
            "metadata": metadata or {}
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def search_similar(self, query_vector: List[float], k: int = 5, role_id: int = 4) -> List[Dict[str, Any]]:
        """Search for similar vectors in the index."""
        url = f"{self.base_url}/search"
        data = {
            "vector": query_vector,
            "k": k,
            "role_id": role_id
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the FAISS index."""
        url = f"{self.base_url}/status"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()

    def clear_index(self) -> Dict[str, Any]:
        """Clear all vectors from the index."""
        url = f"{self.base_url}/clear"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()

    def add_vectors_batch(self, vectors_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add multiple vectors to the index."""
        results = []
        for data in vectors_data:
            try:
                result = self.add_vector(data["id"], data["vector"], data.get("metadata", {}))
                results.append(result)
            except Exception as e:
                results.append({"error": str(e), "id": data.get("id", "unknown")})
        return results

    def get_all_vectors(self) -> List[Dict[str, Any]]:
        """Get all vectors in the index."""
        url = f"{self.base_url}/get_all"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()["vectors"]

    def is_healthy(self) -> bool:
        """Check if the FAISS service is healthy."""
        try:
            self.get_status()
            return True
        except:
            return False

    def load_documents(self, data_dir: str = RAG_DATA_PATH) -> Dict[str, Any]:
        """Load documents from directory into FAISS and MongoDB."""
        model = SentenceTransformer('all-MiniLM-L6-v2')
        mongo_client = MongoDBClient(uri=MONGODB_URI, database_name=DATABASE_NAME)

        loaded_count = 0
        for filename in os.listdir(data_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(data_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read().strip()

                role = filename.split('_')[0]
                role_id = ROLE_MAPPING.get(role)

                chunks = split_text_with_overlap(content, MAX_CHUNK_SIZE, OVERLAP_SIZE)

                print(f"Processing {filename}: {len(chunks)} chunks")

                for chunk_idx, chunk in enumerate(chunks):
                    embedding = model.encode(chunk).tolist()
                    chunk_id = f"{filename}_{chunk_idx + 1}"

                    self.add_vector(chunk_id, embedding, metadata={'role_id': role_id})

                    Document.create_document(
                        mongo_client,
                        title=f"{filename} - Chunk {chunk_idx + 1}",
                        content=chunk,
                        source=filename,
                        metadata={
                            'faiss_id': chunk_id,
                            'chunk_index': chunk_idx,
                            'total_chunks': len(chunks),
                            'original_file': filename
                        },
                        role_id=role_id
                    )

                    loaded_count += 1
                    print(f"Processed chunk: {chunk_id}")

        return {"message": f"Loaded {loaded_count} chunks from documents"}