import sys
sys.path.insert(0, 'src')

from config.settings import MONGODB_URI, DATABASE_NAME
from clients.mongodb.mongodb_client import MongoDBClient
from services.database.models.document_model import Document

def main():
    # Initialize MongoDB client using settings
    client = MongoDBClient(uri=MONGODB_URI, database_name=DATABASE_NAME)

    try:
        # Retrieve all documents
        documents = Document.get_all_documents(client)

        # Print the documents
        print(f"Total documents found: {len(documents)}")
        for doc in documents:
            print(f"ID: {doc._id}")
            print(f"Title: {doc.title}")
            print(f"Content: {doc.content[:100]}...")  # Print first 100 chars
            print(f"Source: {doc.source}")
            print(f"Created At: {doc.created_at}")
            print("-" * 50)

    except Exception as e:
        print(f"Error retrieving documents: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()