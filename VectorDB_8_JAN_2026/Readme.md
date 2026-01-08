VectorDB Question Answering System (FastAPI + ChromaDB + Ollama)

This project implements a local-first Vector Database–powered Question Answering system using FastAPI, ChromaDB, and Ollama embedding models.
It supports document ingestion (PDF / TXT), semantic vector search, and inspection of stored embeddings via API endpoints.

The entire system is designed to run locally, persist data on disk, and be safely published to GitHub without exposing any URLs or secrets.

Architecture Overview
User → FastAPI → Embedding Model (Ollama)
                ↓
            ChromaDB (Persistent)
                ↓
        Vector Search / Retrieval

Project Structure
VectorDB_7_JAN_2026/
│
├── app/
│   ├── main.py                 # FastAPI app entrypoint
│   ├── config.py               # Configuration (paths, collection name)
│   ├── chroma.py               # ChromaDB client & collection
│   ├── document_loader.py      # PDF / TXT loaders
│   ├── text_splitter.py        # Chunking logic
│   ├── embeddings.py           # Ollama embedding wrapper
│   └── router/
│       └── vector.py           # All vector-related API routes
│
├── scripts/
│   └── export_chunks_to_excel.py   # One-time utility script
│
├── tests/
│   ├── conftest.py
│   └── test_vector_api.py
│
├── requirements.txt
├── .gitignore
└── README.md

Features

Local vector database using ChromaDB

Persistent storage (SQLite + Parquet)

Document ingestion (PDF / TXT)

Automatic text chunking

Semantic vector search

Read-only dump endpoint for debugging

Pytest-based API tests

No external URLs or API keys committed

Prerequisites

Python 3.10 or 3.11 (recommended)

Ollama installed locally

Virtual environment (venv)

⚠️ Python 3.13+ and 3.14 are not supported by NumPy / ChromaDB yet.

Setup Instructions
1. Clone the Repository
git clone <your-repo-url>
cd VectorDB_7_JAN_2026

2. Create and Activate Virtual Environment
python -m venv venv


Windows

venv\Scripts\activate


Linux / macOS

source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

Running the Application
uvicorn app.main:app --reload


The API will be available at:

http://127.0.0.1:8000


Swagger UI:

http://127.0.0.1:8000/docs

API Endpoints
Ingest a Document
POST /vector/ingest


Accepts PDF or TXT via multipart upload

Splits text into chunks

Stores embeddings in ChromaDB

Ask a Question (Vector Search)
POST /vector/ask


Example payload:

{
  "query": "What are the privacy challenges of EHRs?"
}


Returns the most relevant document chunks.

Dump Collection (Debugging)
GET /vector/dump


Returns:

Total vector count

Stored chunks

Document IDs

This endpoint is intended for development and verification only.

Where the Vector Data Is Stored

ChromaDB persists data to the directory defined in:

CHROMA_PERSIST_DIR


Example:

app/chroma_db/
 ├── chroma.sqlite3
 ├── chroma-collections.parquet
 └── chroma-embeddings.parquet


If these files do not exist, vectors were not ingested.

Export Chunks to Excel (One-Time Utility)

The script exports all stored chunks into an Excel file.

Run from Project Root
python -m scripts.export_chunks_to_excel


Output:

chunks.xlsx

Running Tests
pytest -v


Tests validate:

API startup

Vector ingestion

Vector search

Collection state

Common Issues & Fixes
collection.count() == 0

Ingestion failed

collection.add() was never executed

client.persist() was not called

No module named app

Always run commands from project root

Do not cd into app/

Design Principles

Local-first, privacy-safe

No hardcoded URLs

No secrets in code

Deterministic persistence

Clear separation of concerns (routers, services, scripts)

Future Enhancements

RAG-based answer synthesis

Authentication middleware

Metadata-based filtering

Chunk re-ranking

Collection statistics endpoint

License

This project is intended for educational and research purposes.