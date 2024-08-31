from pydantic import BaseModel
from typing import Optional
import uuid


class EquipmentBase(BaseModel):
    name: str
    qr_code_uuid: Optional[uuid.UUID] = None


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentResponse(EquipmentBase):
    id: int
