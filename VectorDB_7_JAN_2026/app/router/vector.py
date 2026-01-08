from fastapi import APIRouter,UploadFile,File
from app.schemas import TextItem, Query,embed
from app.embedding import get_embedding,embed_chunking,vector_search
from app.chroma import collection
from app.document_loader import load_pdf,load_txt
from app.chunking import chunk_text

router = APIRouter(prefix="/vector", tags=["Vector"])

@router.post("/upsert")
def upsert(item: TextItem):
    embedding = get_embedding(item.text)

    collection.add(
        ids=[item.id],
        documents=[item.text],
        embeddings=[embedding]
    )

    return {"status": "inserted"}

@router.post("/search")
def search(query: Query):
    embedding = get_embedding(query.query)

    results = collection.query(
        query_embeddings=[embedding],
        n_results=query.top_k
    )

    return [
        {
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "score": results["distances"][0][i]
        }
        for i in range(len(results["ids"][0]))
    ]

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    content = await file.read()

    if file.filename.endswith(".pdf"):
        text = load_pdf(content)
    elif file.filename.endswith(".txt"):
        text = load_txt(content)
    else:
        return {"error": "Unsupported file type"}

    chunks = chunk_text(text)
    embed_chunking(chunks, source=file.filename)

    return {
        "file": file.filename,
        "chunks_stored": len(chunks)
    }

@router.post("/ask")
def ask_question(payload: Query):
    results = vector_search(
        query=payload.query,
        top_k=payload.top_k
    )

    return {
        "question": payload.query,
        "answers": results
    }
