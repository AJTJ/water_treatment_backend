import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.equipment_request import EquipmentRequestStatus


class EquipmentRequestBase(BaseModel):
    id: uuid.UUID
    description: Optional[str] = None
    status: EquipmentRequestStatus
    employee_name: Optional[str] = None
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime
    equipment_id: uuid.UUID


class EquipmentRequestCreate(EquipmentRequestBase):
    pass


class EquipmentRequestUpdate(EquipmentRequestBase):
    pass


class EquipmentRequestResponse(EquipmentRequestBase):
    pass


class EquipmentRequestWithEquipmentInfo(EquipmentRequestBase):
    equipment_name: str
