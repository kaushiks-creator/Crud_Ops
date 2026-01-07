import chromadb
from chromadb.config import Settings
from app.config import CHROMA_COLLECTION, CHROMA_PERSIST_DIR

client = chromadb.Client(
    Settings(
        persist_directory=CHROMA_PERSIST_DIR
    )
)

collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION
)
