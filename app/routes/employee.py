from fastapi import APIRouter, HTTPException
from app.database import collection
from app.models import Employee
from bson import ObjectId

router = APIRouter(prefix="/employee", tags=["Employee"])

@router.post("/")
def create_employee(employee: Employee):
    result = collection.insert_one(employee.dict())
    return {"Inserted_ID": str(result.inserted_id)}

@router.get("/")
def read_employees():
    employees = []
    for emp in collection.find():
        emp["_id"] = str(emp["_id"])
        employees.append(emp)
    return employees

@router.get("/employee/{employee_id}")
def read_employee(employee_id: str):
    employee = collection.find_one({"_id": ObjectId(employee_id)})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee["id"] = str(employee["_id"])
    return employee

@router.put("/employee/{employee_id}")
def update_employee(employee_id: str, employee: Employee):
    result = collection.update_one({"_id": ObjectId(employee_id)}, {"$set": employee.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"Updated_Count": True}

@router.delete("/employee/{employee_id}")
def delete_employee(employee_id: str):
    result = collection.delete_one({"_id": ObjectId(employee_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"Deleted": True}