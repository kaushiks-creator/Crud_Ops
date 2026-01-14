from fastapi import FastAPI
from app.db.qdrant import init_collection
from app.api.routers.health import router as health_router
from app.api.routers.ingest import router as ingest_router

app = FastAPI(title="Crypto Researcher")

@app.on_event("startup")
def startup_event():
    init_collection()

app.include_router(health_router)
app.include_router(ingest_router)  
