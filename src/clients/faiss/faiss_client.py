import requests
from typing import List, Dict, Any
import numpy as np

class FAISSClient:
    """FAISS client for vector similarity search operations."""

    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()

    def add_vector(self, vector_id: str, vector: List[float]) -> Dict[str, Any]:
        """Add a vector to the FAISS index."""
        url = f"{self.base_url}/add_vector"
        data = {
            "id": vector_id,
            "vector": vector
        }
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def search_similar(self, query_vector: List[float], k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar vectors in the index."""
        url = f"{self.base_url}/search"
        data = {
            "vector": query_vector,
            "k": k
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
                result = self.add_vector(data["id"], data["vector"])
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