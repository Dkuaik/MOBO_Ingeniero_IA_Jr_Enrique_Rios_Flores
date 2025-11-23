#!/usr/bin/env python3
"""
MongoDB Setup Script for AI API Project
Initializes database collections and indexes for the RAG system.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.clients.mongodb.mongodb_client import MongoDBClient
from src.config.settings import DATABASE_NAME

def setup_database():
    """Initialize MongoDB database with collections and indexes."""
    try:
        # Initialize MongoDB client without auth for init script
        db_client = MongoDBClient(uri="mongodb://localhost:27017", database_name=DATABASE_NAME)

        # Create collections if they don't exist
        collections = ['users', 'documents', 'conversations', 'embeddings', 'counters']

        for collection_name in collections:
            # MongoDB creates collections implicitly, but we can ensure indexes
            collection = db_client.get_collection(collection_name)

            if collection_name == 'users':
                # Create unique index on username and email
                collection.create_index('username', unique=True)
                collection.create_index('email', unique=True)
                print(f"Created indexes for {collection_name} collection")

            elif collection_name == 'documents':
                # Create text index for content search
                collection.create_index([('content', 'text'), ('title', 'text')])
                collection.create_index('source')
                print(f"Created text index for {collection_name} collection")

            elif collection_name == 'conversations':
                # Index for conversation retrieval
                collection.create_index('user_id')
                collection.create_index('created_at')
                print(f"Created indexes for {collection_name} collection")

            elif collection_name == 'embeddings':
                # Index for vector similarity search (placeholder for vector DB integration)
                collection.create_index('document_id')
                print(f"Created indexes for {collection_name} collection")

        print("MongoDB setup completed successfully!")

        # Close connection
        db_client.close()

    except Exception as e:
        print(f"Error setting up MongoDB: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()