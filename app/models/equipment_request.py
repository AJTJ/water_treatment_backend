from re import U
import uuid
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum as PyEnum

from app.schemas.equipment_request import EquipmentRequestStatus


class UrgencyLevels(PyEnum):
    urgent = "urgent"
    not_urgent = "not_urgent"


# TODO Update the database
# Equipment/Part request
class EquipmentRequestBase(BaseModel):
    id: uuid.UUID

    part_name: str
    description: Optional[str] = None
    operator_name: Optional[str] = None
    image_url: Optional[str]

    # part things
    part_number: Optional[str] = None
    quantity: Optional[int] = None
    urgency: UrgencyLevels = UrgencyLevels.not_urgent

    # internal things
    equipment_id: uuid.UUID
    status: EquipmentRequestStatus = EquipmentRequestStatus.ACTIVE
    created_at: datetime
    updated_at: datetime


class EquipmentRequestCreate(BaseModel):
    description: Optional[str] = None
    operator_name: Optional[str] = None
    image_url: Optional[str]
    equipment_id: uuid.UUID


class EquipmentRequestUpdate(BaseModel):
    description: Optional[str] = None
    operator_name: Optional[str] = None
    image_url: Optional[str]


class EquipmentRequestResponse(EquipmentRequestBase):
    pass


class EquipmentRequestWithEquipmentInfo(EquipmentRequestBase):
    equipment_name: str


class ManyEquipmentRequestsResponse(BaseModel):
    total: int
    equipment_requests: List[EquipmentRequestBase]
