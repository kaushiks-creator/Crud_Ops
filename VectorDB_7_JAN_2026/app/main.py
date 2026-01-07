from fastapi import FastAPI
from app.router.vector import router as vector_router
app = FastAPI(title="Vector Database API")

app.include_router(vector_router)