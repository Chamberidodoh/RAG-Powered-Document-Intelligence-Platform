from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_upload_and_delete_documents(client: TestClient) -> None:
    upload_response = client.post(
        "/api/v1/documents/upload",
        files=[("files", ("sample.txt", b"This is sample content for testing.", "text/plain"))],
    )
    assert upload_response.status_code == 200
