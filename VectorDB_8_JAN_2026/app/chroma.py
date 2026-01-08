import chromadb
from chromadb.config import Settings
from app.config import CHROMA_COLLECTION, CHROMA_PERSIST_DIR

client = chromadb.Client(
    Settings(
        persist_directory=str(CHROMA_PERSIST_DIR),
        anonymized_telemetry=False,
    )
)

collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    metadata={"hnsw:space": "cosine"}
)
