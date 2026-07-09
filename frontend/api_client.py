import os
from typing import Any

import requests

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def health() -> dict[str, Any]:
    response = requests.get(f"{API_BASE_URL}/api/v1/health", timeout=10)
    response.raise_for_status()
    return response.json()


def upload_documents(files: list[Any]) -> list[dict[str, Any]]:
    form_data: list[tuple[str, Any]] = []
    for uploaded_file in files:
        form_data.append(("files", (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)))
    response = requests.post(f"{API_BASE_URL}/api/v1/documents/upload", files=form_data, timeout=60)
    response.raise_for_status()
    return response.json()


def list_documents() -> list[dict[str, Any]]:
    response = requests.get(f"{API_BASE_URL}/api/v1/documents", timeout=10)
    response.raise_for_status()
    return response.json()


def delete_document(document_id: str) -> dict[str, Any]:
    response = requests.delete(f"{API_BASE_URL}/api/v1/documents/{document_id}", timeout=10)
    response.raise_for_status()
    return response.json()


def query_chat(payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(f"{API_BASE_URL}/api/v1/chat/query", json=payload, timeout=60)
    response.raise_for_status()
    return response.json()
