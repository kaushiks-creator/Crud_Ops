import io
from fastapi.testclient import TestClient
from app.main import app
from app.chroma import collection

client = TestClient(app)


def test_document_ingestion_txt():
    initial_count = collection.count()

    text_content = """
    Electronic Health Records improve clinical decision making
    but raise serious privacy and security concerns.
    """

    file = {
        "file": (
            "ehr_test.txt",
            io.BytesIO(text_content.encode("utf-8")),
            "text/plain",
        )
    }

    response = client.post("/vector/ingest", files=file)

    assert response.status_code == 200

    data = response.json()

    assert "chunks_stored" in data
    assert data["chunks_stored"] > 0

    new_count = collection.count()
    assert new_count > initial_count
