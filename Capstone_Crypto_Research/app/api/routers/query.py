from fastapi import APIRouter
from pydantic import BaseModel
from app.services.embedding_service import embed_text
from app.services.search_service import semantic_search
from app.services.llm_service import summarize_articles

router = APIRouter(prefix="/query", tags=["Query"])


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/search")
def search_news(payload: SearchRequest):
    query_vector = embed_text(payload.query)
    results = semantic_search(query_vector, payload.top_k)

    return {
        "query": payload.query,
        "results": results
    }



@router.post("/summarize")
def summarize(payload: SearchRequest):
    query_vector = embed_text(payload.query)
    results = semantic_search(query_vector, payload.top_k)

    summary = summarize_articles(payload.query, results)

    return {
        "query": payload.query,
        "summary": summary,
        "sources": results
    }
