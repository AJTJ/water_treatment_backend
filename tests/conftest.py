# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app  # Import the FastAPI app
from typing import Generator


@pytest.fixture(scope="module")
def test_client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
