import os
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message="Using `httpx` with `starlette.testclient` is deprecated")
warnings.filterwarnings("ignore", message="'asyncio.iscoroutinefunction' is deprecated")

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client() -> TestClient:
    os.environ.setdefault("OPENAI_API_KEY", "test-key")
    return TestClient(app)
