from fastapi.testclient import TestClient


def test_chat_query_endpoint_returns_response(client: TestClient) -> None:
    payload = {"question": "What is in the document?"}
    response = client.post("/api/v1/chat/query", json=payload)
    assert response.status_code == 200
