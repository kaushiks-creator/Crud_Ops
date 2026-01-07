from fastapi import APIRouter
from app.schemas import TextItem, Query
from app.embedding import get_embedding
from app.chroma import collection

router = APIRouter(prefix="/vector", tags=["Vector"])

@router.post("/upsert")
def upsert(item: TextItem):
    embedding = get_embedding(item.text)

    collection.add(
        ids=[item.id],
        documents=[item.text],
        embeddings=[embedding]
    )

    return {"status": "inserted"}

@router.post("/search")
def search(query: Query):
    embedding = get_embedding(query.query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=query.top_k
    )

    return [
        {
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "score": results["distances"][0][i]
        }
        for i in range(len(results["ids"][0]))
    ]
