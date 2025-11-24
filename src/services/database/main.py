#!/usr/bin/env python3
"""
Main database module for MongoDB setup and operations.
Provides initialization, sample data loading, and database management.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.clients.mongodb import MongoDBClient
from src.services.database.models.user_model import User
from src.services.database.models.document_model import Document
from src.config.settings import MONGODB_URI, DATABASE_NAME, RAG_DATA_PATH

def initialize_database():
    """Initialize MongoDB database with sample data."""
    print("Initializing MongoDB database...")

    try:
        # Cliente de mongo db para comunicación
        db_client = MongoDBClient(uri=MONGODB_URI, database_name=DATABASE_NAME)

        # Creación de un user
        print("Creating sample user...")
        sample_user = User.create_user(
            db_client=db_client,
            username="admin",
            email="admin@aiapi.com",
            password_hash="123" 
        )
        print(f"Created user: {sample_user.username}")

        # Carga de algunos docs dummy
        print("Loading sample documents...")
        rag_path = Path(project_root) / RAG_DATA_PATH
        if rag_path.exists():
            for txt_file in rag_path.glob("*.txt"):
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                doc = Document.create_document(
                    db_client=db_client,
                    title=txt_file.stem.replace('_', ' ').title(),
                    content=content,
                    source=str(txt_file.relative_to(project_root)),
                    metadata={"file_size": txt_file.stat().st_size}
                )
                print(f"Loaded document: {doc.title}")

        print("Database initialization completed successfully!")

        # Close connection
        db_client.close()

    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

def test_database_connection():
    """Test MongoDB connection and basic operations."""
    print("Testing MongoDB connection...")

    try:
        db_client = MongoDBClient(uri=MONGODB_URI, database_name=DATABASE_NAME)

        # Test user operations
        user = User.find_user_by_username(db_client, "admin")
        if user:
            print(f"Found user: {user.username} ({user.email})")

        # Test document operations
        documents = Document.get_all_documents(db_client)
        print(f"Found {len(documents)} documents in database")
        for doc in documents[:3]:  # Show first 3
            print(f"  - {doc.title}: {doc.content[:50]}...")

        # Test search
        search_results = Document.find_documents_by_content(db_client, "AI")
        print(f"Search for 'AI' returned {len(search_results)} results")

        db_client.close()
        print("Database connection test completed successfully!")

    except Exception as e:
        print(f"Database connection test failed: {e}")
        sys.exit(1)

def main():
    """Main function for database operations."""
    import argparse

    parser = argparse.ArgumentParser(description="MongoDB Database Manager")
    parser.add_argument("action", choices=["init", "test", "setup"],
                       help="Action to perform: init (initialize with sample data), test (test connection), setup (run setup script)")

    args = parser.parse_args()

    if args.action == "init":
        initialize_database()
    elif args.action == "test":
        test_database_connection()
    elif args.action == "setup":
        # Run the setup script
        os.system("python scripts/setup_mongodb.py")

if __name__ == "__main__":
    main()