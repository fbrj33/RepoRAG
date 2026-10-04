from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_index_rejects_missing_repo_url():
    response = client.post("/repositories/index", json={})

    assert response.status_code == 422


def test_ask_rejects_missing_fields():
    response = client.post("/ask", json={})

    assert response.status_code == 422


def test_unknown_endpoint():
    response = client.get("/unknown")

    assert response.status_code == 404