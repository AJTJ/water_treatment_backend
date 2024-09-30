from fastapi.testclient import TestClient
from typing import Dict


def test_get_many_item(test_client: TestClient) -> None:
    response = test_client.get("/v1/item/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_item(test_client: TestClient) -> None:
    new_item: Dict[str, str] = {
        "name": "Pump A",
        "location": "Plant 1",
        "description": "High capacity pump",
        "status": "Active",
    }
    response = test_client.post("/v1/item/", json=new_item)
    assert response.status_code == 201
    assert response.json()["name"] == "Pump A"
