# tests/test_qr_code.py
from fastapi.testclient import TestClient
from typing import Any, Dict


def test_create_qr_code(test_client: TestClient) -> None:
    new_qr_code: Dict[str, Any] = {
        "batch_number": 1,
        "full_url": "https://yourdomain.com/qr/123e4567-e89b-12d3-a456-426614174000",
        "status": "Active",
    }
    response = test_client.post("/v1/qr_code/", json=new_qr_code)
    assert response.status_code == 201
    assert response.json()["status"] == "Active"


def test_get_qr_codes(test_client: TestClient) -> None:
    response = test_client.get("/v1/qr_code/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
