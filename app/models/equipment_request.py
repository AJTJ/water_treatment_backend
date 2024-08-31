import uuid
from pydantic import BaseModel
from typing import Optional


class EquipmentRequestBase(BaseModel):
    description: Optional[str] = None
    equipment_id: uuid.UUID


class EquipmentRequestCreate(EquipmentRequestBase):
    pass


class EquipmentRequestUpdate(EquipmentRequestBase):
    pass


class EquipmentRequestResponse(EquipmentRequestBase):
    id: uuid.UUID
