import os
import sys
sys.path.insert(0, 'src')
from sentence_transformers import SentenceTransformer
from clients.faiss.faiss_client import FAISSClient
from clients.mongodb.mongodb_client import MongoDBClient
from services.database.models.document_model import Document
from config.settings import MONGODB_URI, DATABASE_NAME, RAG_DATA_PATH



# Configuration for chunking
MAX_CHUNK_SIZE = 1000  # Maximum characters per chunk
OVERLAP_SIZE = 200     # Characters of overlap between chunks

# Role to role_id mapping
ROLE_MAPPING = {
    "ADMIN": 1,
    "DEV": 2,
    "HR": 3,
    "ALL": 4
}

def split_text_with_overlap(text: str, max_chunk_size: int, overlap_size: int):
    """Split text into chunks with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chunk_size
        if end < len(text):
            # Find a good break point (sentence end or space)
            # For simplicity, just cut at max_chunk_size
            chunk = text[start:end]
        else:
            chunk = text[start:]
        chunks.append(chunk)
        start = end - overlap_size
        if start >= len(text):
            break
    return chunks

def load_embeddings():
    # Initialize the sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Initialize clients
    faiss_client = FAISSClient()
    mongo_client = MongoDBClient(uri=MONGODB_URI, database_name=DATABASE_NAME)

    # Directory containing the documents
    data_dir = RAG_DATA_PATH

    # Process each document
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            # Extract role from filename
            role = filename.split('_')[0]
            role_id = ROLE_MAPPING.get(role)

            # Split content into chunks with overlap
            chunks = split_text_with_overlap(content, MAX_CHUNK_SIZE, OVERLAP_SIZE)

            print(f"Processing {filename}: {len(chunks)} chunks")

            # Process each chunk
            for chunk_idx, chunk in enumerate(chunks):
                # Generate embedding for the chunk
                embedding = model.encode(chunk).tolist()

                # Create unique ID for the chunk
                chunk_id = f"{filename}_{chunk_idx + 1}"

                # Add to FAISS
                faiss_client.add_vector(chunk_id, embedding)

                # Save chunk to MongoDB
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

                print(f"Processed chunk: {chunk_id}")

if __name__ == "__main__":
    load_embeddings()