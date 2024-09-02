# tests/test_equipment.py
from fastapi.testclient import TestClient
from typing import Dict


def test_get_all_equipments(test_client: TestClient) -> None:
    response = test_client.get("/v1/equipment/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_equipment(test_client: TestClient) -> None:
    new_equipment: Dict[str, str] = {
        "name": "Pump A",
        "location": "Plant 1",
        "description": "High capacity pump",
        "status": "Active",
    }
    response = test_client.post("/v1/equipment/", json=new_equipment)
    assert response.status_code == 201
    assert response.json()["name"] == "Pump A"
