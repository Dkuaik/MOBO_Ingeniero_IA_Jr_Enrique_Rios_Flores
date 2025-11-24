import pytest
from unittest.mock import patch, MagicMock
from src.clients.mongodb.mongodb_client import MongoDBClient


class TestMongoDBClient:
    """Test MongoDB client."""

    @patch('src.clients.mongodb.mongodb_client.MongoClient')
    def test_init_success(self, mock_mongo_client):
        """Test successful MongoDB client initialization."""
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client

        client = MongoDBClient()

        mock_mongo_client.assert_called_once_with("mongodb://localhost:27017")
        assert client.client == mock_client
        assert client.db == mock_client["ai_api_db"]

    @patch('src.clients.mongodb.mongodb_client.MongoClient')
    def test_init_connection_failure(self, mock_mongo_client):
        """Test MongoDB client initialization with connection failure."""
        mock_mongo_client.side_effect = Exception("Connection failed")

        with pytest.raises(Exception, match="Connection failed"):
            MongoDBClient()

    def test_get_collection(self):
        """Test getting a collection."""
        with patch('src.clients.mongodb.mongodb_client.MongoClient') as mock_mongo_client:
            mock_client = MagicMock()
            mock_db = MagicMock()
            mock_client.__getitem__.return_value = mock_db
            mock_mongo_client.return_value = mock_client

            client = MongoDBClient()
            collection = client.get_collection("test_collection")

            mock_db.__getitem__.assert_called_once_with("test_collection")
            assert collection == mock_db["test_collection"]

    def test_insert_document(self):
        """Test inserting a document."""
        with patch('src.clients.mongodb.mongodb_client.MongoClient') as mock_mongo_client:
            mock_client = MagicMock()
            mock_db = MagicMock()
            mock_collection = MagicMock()
            mock_db.__getitem__.return_value = mock_collection
            mock_client.__getitem__.return_value = mock_db
            mock_mongo_client.return_value = mock_client

            client = MongoDBClient()
            result = client.insert_document("test_collection", {"key": "value"})

            mock_collection.insert_one.assert_called_once_with({"key": "value"})
            assert result == mock_collection.insert_one.return_value

    def test_find_documents(self):
        """Test finding documents."""
        with patch('src.clients.mongodb.mongodb_client.MongoClient') as mock_mongo_client:
            mock_client = MagicMock()
            mock_db = MagicMock()
            mock_collection = MagicMock()
            mock_collection.find.return_value = [{"doc1": "value1"}, {"doc2": "value2"}]
            mock_db.__getitem__.return_value = mock_collection
            mock_client.__getitem__.return_value = mock_db
            mock_mongo_client.return_value = mock_client

            client = MongoDBClient()
            documents = client.find_documents("test_collection", {"query": "value"})

            mock_collection.find.assert_called_once_with({"query": "value"})
            assert documents == [{"doc1": "value1"}, {"doc2": "value2"}]

    def test_find_documents_no_query(self):
        """Test finding documents without query."""
        with patch('src.clients.mongodb.mongodb_client.MongoClient') as mock_mongo_client:
            mock_client = MagicMock()
            mock_db = MagicMock()
            mock_collection = MagicMock()
            mock_collection.find.return_value = [{"doc1": "value1"}]
            mock_db.__getitem__.return_value = mock_collection
            mock_client.__getitem__.return_value = mock_db
            mock_mongo_client.return_value = mock_client

            client = MongoDBClient()
            documents = client.find_documents("test_collection")

            mock_collection.find.assert_called_once_with({})
            assert documents == [{"doc1": "value1"}]

    def test_close(self):
        """Test closing the connection."""
        with patch('src.clients.mongodb.mongodb_client.MongoClient') as mock_mongo_client:
            mock_client = MagicMock()
            mock_mongo_client.return_value = mock_client

            client = MongoDBClient()
            client.close()

            mock_client.close.assert_called_once()