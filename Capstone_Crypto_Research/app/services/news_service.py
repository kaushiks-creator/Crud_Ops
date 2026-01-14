import requests
from app.core.config import NEWS_API_KEY, NEWS_API_URL

CRYPTO_QUERY = "crypto OR bitcoin OR ethereum OR blockchain"
PAGE_SIZE = 20


def fetch_crypto_news() -> list[dict]:
    params = {
        "q": CRYPTO_QUERY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": PAGE_SIZE,
        "apiKey": NEWS_API_KEY,
    }

    response = requests.get(NEWS_API_URL, params=params, timeout=10)
    response.raise_for_status()

    return response.json().get("articles", [])
