import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from typing import Dict


@pytest.fixture
def example_item_request() -> Dict[str, str]:
    return {
        "item_id": "123e4567-e89b-12d3-a456-426614174000",
        "description": "Need new filter",
        "request_date": datetime.now().isoformat(),
        "status": "Active",
    }


def test_create_item_request(
    test_client: TestClient, example_item_request: Dict[str, str]
) -> None:
    response = test_client.post("/v1/item_request/", json=example_item_request)
    assert response.status_code == 201
    assert response.json()["description"] == "Need new filter"
    assert response.json()["status"] == "Active"
