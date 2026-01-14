from fastapi import APIRouter
from app.services.news_service import fetch_crypto_news
from app.services.normalizer import normalize_article
from app.db.qdrant import upsert_articles
from app.services.embedding_service import embed_text

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/news")
def ingest_news():
    raw_articles = fetch_crypto_news()
    normalized = []

    for article in raw_articles:
        norm = normalize_article(article)
        embedding = embed_text(
            f"{norm['title']} {norm['content']}"
        )
        norm["vector"] = embedding
        normalized.append(norm)

    count = upsert_articles(normalized)

    return {"status": "success", "ingested": count}
