import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION")
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "chroma_db")

if not OLLAMA_MODEL:
    raise RuntimeError("OLLAMA_MODEL missing")

if not CHROMA_COLLECTION:
    raise RuntimeError("CHROMA_COLLECTION missing")
