"""
Configuration settings for the AI API project.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ai_api_db")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# AI Client Configuration
OPENROUTER_API_KEY = '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'
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "x-ai/grok-code-fast-1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY","apikey")
ANTHROPIC_API_KEY= os.getenv("ANTHROPIC_API_KEY","apikey")

# Embedding Configuration
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "1536"))

# RAG Configuration
RAG_DATA_PATH = os.getenv("RAG_DATA_PATH", "docs")
MAX_RETRIEVED_DOCUMENTS = int(os.getenv("MAX_RETRIEVED_DOCUMENTS", "5"))
ROLE_MAPPING = {
    "ADMIN": 1,
    "DEV": 2,
    "HR": 3,
    "ALL": 4
}