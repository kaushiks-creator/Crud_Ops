from fastapi import FastAPI,HTTPException
from app.routes.employee import router as employee_router

app = FastAPI()
@app.get("/")
def hello():
    return {"Message": "Welcome to FastAPI CRUD Operations"}

app.include_router(employee_router)
