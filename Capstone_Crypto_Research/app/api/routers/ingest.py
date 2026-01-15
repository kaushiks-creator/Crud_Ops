from fastapi import APIRouter, BackgroundTasks
from app.services.news_service import fetch_crypto_news
from app.services.normalizer import normalize_article
from app.db.qdrant import upsert_articles
from app.services.embedding_service import embed_text
from app.services.sentiment_service import classify_sentiment

router = APIRouter(prefix="/ingest", tags=["Ingestion"])


def ingest_job():
    raw_articles = fetch_crypto_news()
    normalized = []

    for article in raw_articles:
        norm = normalize_article(article)

        text = f"{norm['title']} {norm['content']}"

        norm["sentiment"] = classify_sentiment(text)
        norm["vector"] = embed_text(text)

        normalized.append(norm)

    upsert_articles(normalized)


@router.post("/news")
def ingest_news(background_tasks: BackgroundTasks):
    background_tasks.add_task(ingest_job)
    return {
        "status": "started",
        "message": "News ingestion running in background"
    }
