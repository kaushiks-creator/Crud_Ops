# VectorDB Question Answering System

A local-first Question Answering system built using FastAPI, ChromaDB, and Ollama embeddings. The system supports ingesting PDF and TXT documents, storing them as vectors with persistent storage, and performing semantic search over the stored content.

The application is designed to run completely locally, without exposing external URLs or secrets, and is suitable for publishing on GitHub.

## Stack
Python 3.10 / 3.11  
FastAPI  
ChromaDB (persistent)  
Ollama embeddings  
Pytest  

## Structure
VectorDB_7_JAN_2026/
app/ – FastAPI application code  
scripts/ – one-time utility scripts  
tests/ – pytest test cases  

## Setup
python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  

## Run
uvicorn app.main:app --reload  

Swagger UI available at `/docs`.

## API
POST /vector/ingest – ingest PDF or TXT documents  
POST /vector/ask – semantic vector search  
GET /vector/dump – inspect stored chunks (development only)  

## Export Stored Chunks
python -m scripts.export_chunks_to_excel  

## Tests
pytest -v  

## Notes
Run all commands from the project root.  
ChromaDB data is stored locally using SQLite and Parquet files.
