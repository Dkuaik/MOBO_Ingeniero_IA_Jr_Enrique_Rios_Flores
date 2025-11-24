import pytest
from src.clients.faiss.faiss_client import FAISSClient


class TestFAISSClient:
    """Test FAISS client."""

    def test_init(self):
        """Test FAISS client initialization."""
        client = FAISSClient()
        assert client.base_url == "http://localhost:8001"

    def test_init_custom_url(self):
        """Test FAISS client with custom URL."""
        client = FAISSClient("http://custom:9000")
        assert client.base_url == "http://custom:9000"

    def test_add_vector(self):
        """Test adding a vector (integration test)."""
        client = FAISSClient()
        vector = [0.1] * 384  # FAISS expects 384-dim vectors
        result = client.add_vector("test_id", vector)
        assert "message" in result

    def test_search_similar(self):
        """Test searching similar vectors (integration test)."""
        client = FAISSClient()
        query_vector = [0.1] * 384
        results = client.search_similar(query_vector, k=5)
        assert isinstance(results, list)

    def test_get_status(self):
        """Test getting status (integration test)."""
        client = FAISSClient()
        status = client.get_status()
        assert "total_vectors" in status

    def test_clear_index(self):
        """Test clearing index (integration test)."""
        client = FAISSClient()
        result = client.clear_index()
        assert "message" in result

    def test_add_vectors_batch(self):
        """Test adding vectors in batch (integration test)."""
        client = FAISSClient()
        vectors_data = [
            {"id": "test1", "vector": [0.1] * 384},
            {"id": "test2", "vector": [0.2] * 384}
        ]
        results = client.add_vectors_batch(vectors_data)
        assert len(results) == 2

    def test_get_all_vectors(self):
        """Test getting all vectors (integration test)."""
        client = FAISSClient()
        vectors = client.get_all_vectors()
        assert isinstance(vectors, list)

    def test_is_healthy(self):
        """Test health check (integration test)."""
        client = FAISSClient()
        healthy = client.is_healthy()
        assert isinstance(healthy, bool)