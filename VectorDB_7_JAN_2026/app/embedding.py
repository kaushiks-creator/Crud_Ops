import requests
from app.config import OLLAMA_URL

MODEL = "nomic-embed-text"

def get_embedding(text: str) -> list[float]:
    response = requests.post(
        f"{OLLAMA_URL}/v1/models/{MODEL}/embed",
        json={"model": MODEL, "prompt": text})
    response.raise_for_status()
    embedding = response.json().get("embedding")
