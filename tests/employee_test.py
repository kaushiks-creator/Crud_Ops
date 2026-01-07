from fastapi.testclient import TestClient
from app.main import app

client_1 = TestClient(app)

def test_create():
    response = client_1.post(
        "/employee/",
        json={
            "id": "1",
            "name": "Kaushik",
            "mail": "Kaush@xyz.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "Inserted_ID" in data

def test_read():
    response = client_1.get("/employee/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)