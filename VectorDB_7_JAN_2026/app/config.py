import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL")
VECTOR_DB_PATH = os.getenv("CHROMA_PERSIST_DIR")

if not OLLAMA_URL:
    raise ValueError("OLLAMA_BASE_URL environment variable is not set.")
if not VECTOR_DB_PATH:   
    raise ValueError("CHROMA_PERSIST_DIR environment variable is not set.")
