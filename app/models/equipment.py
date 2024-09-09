from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid

from app.schemas.equipment import EquipmentStatus


class EquipmentBase(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    equipment_model_number: Optional[str] = None
    location: Optional[str] = None
    image_url: Optional[str] = None
    status: EquipmentStatus
    created_at: datetime
    updated_at: datetime


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentResponse(EquipmentBase):
    pass
