# app/models/__init__.py
from app.schemas.equipment import Equipment
from app.schemas.equipment_request import EquipmentRequest

__all__ = ["Equipment", "EquipmentRequest"]
