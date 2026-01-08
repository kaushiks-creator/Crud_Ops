import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION")
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CHROMA_PERSIST_DIR = str(BASE_DIR / "chroma_db")


if not OLLAMA_MODEL:
    raise RuntimeError("OLLAMA_MODEL missing")

if not CHROMA_COLLECTION:
    raise RuntimeError("CHROMA_COLLECTION missing")
