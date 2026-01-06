from pydantic import BaseModel

class Employee(BaseModel):
    id: int
    name: str
    mail: str