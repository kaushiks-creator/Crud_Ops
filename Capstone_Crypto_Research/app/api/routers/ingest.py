from fastapi import APIRouter
from app.services.news_service import fetch_crypto_news
from app.services.normalizer import normalize_article
from app.db.qdrant import upsert_articles

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


@router.post("/news")
def ingest_news():
    raw_articles = fetch_crypto_news()
    normalized = [normalize_article(a) for a in raw_articles]

    count = upsert_articles(normalized)

    return {
        "status": "success",
        "ingested": count,
    }
