import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    os.environ.setdefault("OPENAI_API_KEY", "test-key")
    return TestClient(app)
