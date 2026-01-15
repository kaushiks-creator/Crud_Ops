import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

def classify_sentiment(text: str) -> str:
    prompt = f"""
Classify the sentiment of this crypto news as one word only:
bullish, bearish, or neutral.

Text:
{text[:500]}
"""

    r = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    r.raise_for_status()

    return r.json()["response"].strip().lower()
