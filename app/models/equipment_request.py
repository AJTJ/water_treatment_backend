import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EquipmentRequestBase(BaseModel):
    equipment_id: uuid.UUID
    description: Optional[str] = None
    request_date: datetime
    image_url: Optional[str] = None


class EquipmentRequestCreate(EquipmentRequestBase):
    pass


class EquipmentRequestUpdate(EquipmentRequestBase):
    pass


class EquipmentRequestResponse(EquipmentRequestBase):
    updated_at: datetime


class EquipmentRequestWithEquipmentInfo(EquipmentRequestBase):
    id: uuid.UUID
    equipment_name: str
