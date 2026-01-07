import requests
import ollama
from app.config import OLLAMA_MODEL
from app.chroma import collection

def get_embedding(text: str):
    response = ollama.embeddings(
        model=OLLAMA_MODEL,
        prompt=text
    )

    embedding = response["embedding"]

    collection.add(
        documents=[text],
        embeddings=[embedding],
        ids=[str(hash(text))]
    )

    return embedding
