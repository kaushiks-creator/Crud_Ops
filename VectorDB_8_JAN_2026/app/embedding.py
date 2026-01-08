import requests
import ollama
from app.config import OLLAMA_MODEL
from app.chroma import collection
import uuid

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

def embed_chunking(chunks:list[str],source:str):
    ids = []
    embeddings = []

    for chunk in chunks:
        embeddings.append(get_embedding(chunk))
        ids.append(str(uuid.uuid4()))

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"source":source}]*len(chunks)
    )

def vector_search(query:str,top_k:int = 5):
    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )