from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBClient:
    """MongoDB client for database operations in the AI API project."""

    def __init__(self, uri: str = "mongodb://localhost:27017", database_name: str = "ai_api_db"):
        try:
            self.client = MongoClient(uri)
            self.db = self.client[database_name]
            # Test the connection
            self.client.admin.command('ping')
            print("MongoDB connection successful")
        except ConnectionFailure:
            print("MongoDB connection failed")
            raise

    def get_collection(self, collection_name: str):
        """Get a collection from the database."""
        return self.db[collection_name]

    def insert_document(self, collection_name: str, document: dict):
        """Insert a document into a collection."""
        collection = self.get_collection(collection_name)
        return collection.insert_one(document)

    def find_documents(self, collection_name: str, query: dict = None):
        """Find documents in a collection."""
        collection = self.get_collection(collection_name)
        return list(collection.find(query or {}))

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()