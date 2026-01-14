import hashlib
import uuid


def normalize_article(article: dict) -> dict:
    url = article.get("url")

    url_hash = hashlib.sha256(
        url.encode("utf-8")
    ).hexdigest()

    content = article.get("content") or article.get("description") or ""

    return {
        "id": str(uuid.uuid4()),        # ✅ VALID QDRANT ID
        "url_hash": url_hash,            # ✅ DEDUP KEY
        "title": article.get("title"),
        "content": content,
        "source": article.get("source", {}).get("name"),
        "url": url,
        "published_at": article.get("publishedAt"),
        "asset": "UNKNOWN",
        "topic": "crypto",
        "sentiment": "neutral",
    }
