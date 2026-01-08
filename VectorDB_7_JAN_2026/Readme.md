# Document Ingestion System using FastAPI and ChromaDB

This project implements a local document ingestion pipeline using FastAPI and ChromaDB. It allows PDF and TXT files to be uploaded, processed, split into text chunks, embedded using a local embedding model, and persistently stored in a vector database for later use.

The system is designed to run entirely on a local machine and does not expose any external URLs or credentials, making it safe to publish on GitHub.

## Stack
Python 3.10 / 3.11  
FastAPI  
ChromaDB (persistent)  
Ollama embeddings  
Pytest  

## Structure
VectorDB_7_JAN_2026/
app/ – ingestion logic, loaders, chunking, database  
scripts/ – utility scripts  
tests/ – pytest tests  

## Setup
python -m venv venv  
venv\Scripts\activate  
pip install -r requirements.txt  

## Run
uvicorn app.main:app --reload  

Swagger UI is available at `/docs`.

## Ingestion API
POST /vector/ingest  
Accepts PDF or TXT files via multipart upload, extracts text, splits it into chunks, generates embeddings, and stores them persistently in ChromaDB.

## Export Ingested Chunks
python -m scripts.export_chunks_to_excel  

Exports all stored text chunks into an Excel file for inspection.

## Tests
pytest -v  

## Notes
Run all commands from the project root.  
ChromaDB data is stored locally using SQLite and Parquet files.
