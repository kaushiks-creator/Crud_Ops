from pydantic import BaseModel

class TextItem(BaseModel):
    id: str
    text: str

class Query(BaseModel):
    query: str
    top_k: int = 5
