from typing import Optional
from pydantic import BaseModel
import uuid

from app.schemas.equipment import EquipmentBaseSimple


class SupplierBase(BaseModel):
    id: uuid.UUID
    name: str
    equipment: Optional[list[EquipmentBaseSimple]]


class SupplierBaseSimple(BaseModel):
    id: uuid.UUID
    name: str
