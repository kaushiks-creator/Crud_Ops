from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

COLLECTION_NAME = "crypto_news"
VECTOR_SIZE = 768 

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        host="localhost",
        port=6333
    )


def init_collection() -> None:
    client = get_qdrant_client()

    existing_collections = [
        c.name for c in client.get_collections().collections
    ]

    if COLLECTION_NAME in existing_collections:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE
        )
    )
