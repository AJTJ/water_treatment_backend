import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.equipment_request import EquipmentRequestStatus


class EquipmentRequestBase(BaseModel):
    id: uuid.UUID
    description: Optional[str] = None
    request_date: datetime
    status: EquipmentRequestStatus = EquipmentRequestStatus.ACTIVE
    image_url: Optional[str] = None


class EquipmentRequestCreate(EquipmentRequestBase):
    pass


class EquipmentRequestUpdate(EquipmentRequestBase):
    pass


class EquipmentRequestResponse(EquipmentRequestBase):
    updated_at: datetime


class EquipmentRequestWithEquipmentInfo(EquipmentRequestBase):
    equipment_id: uuid.UUID
    equipment_name: str
    image_url: Optional[str] = None
