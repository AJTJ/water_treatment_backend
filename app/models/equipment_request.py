import uuid
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.equipment_request import EquipmentRequestStatus


class EquipmentRequestBase(BaseModel):
    id: uuid.UUID
    description: Optional[str] = None
    employee_name: Optional[str] = None
    image_url: Optional[str]
    equipment_id: uuid.UUID
    status: EquipmentRequestStatus = EquipmentRequestStatus.ACTIVE
    created_at: datetime
    updated_at: datetime


class EquipmentRequestCreate(BaseModel):
    description: Optional[str] = None
    employee_name: Optional[str] = None
    image_url: Optional[str]
    equipment_id: uuid.UUID


class EquipmentRequestUpdate(BaseModel):
    description: Optional[str] = None
    employee_name: Optional[str] = None
    image_url: Optional[str]


class EquipmentRequestResponse(EquipmentRequestBase):
    pass


class EquipmentRequestWithEquipmentInfo(EquipmentRequestBase):
    equipment_name: str


class ManyEquipmentRequestsResponse(BaseModel):
    total: int
    equipment_requests: List[EquipmentRequestBase]
