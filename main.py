from fastapi import FastAPI,HTTPException
from database import collection
from models import Employee
from bson import ObjectId

app = FastAPI()
@app.get("/")
def hello():
    return {"Message": "Welcome to FastAPI CRUD Operations"}

@app.post("/employee/")
def create_employee(employee: Employee):
    result = collection.insert_one(employee.dict())
    return {"Inserted_ID": str(result.inserted_id)}

@app.get("/employee/")
def read_employees():
    employees = []
    for emp in collection.find():
        emp["_id"] = str(emp["_id"])
        employees.append(emp)
    return employees

@app.get("/employee/{employee_id}")
def read_employee(employee_id: str):
    employee = collection.find_one({"_id": ObjectId(employee_id)})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee["id"] = str(employee["_id"])
    return employee

@app.put("/employee/{employee_id}")
def update_employee(employee_id: str, employee: Employee):
    result = collection.update_one({"_id": ObjectId(employee_id)}, {"$set": employee.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"Updated_Count": True}

@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: str):
    result = collection.delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"Deleted": True}