import uuid
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.schemas.equipment_request import EquipmentRequestStatus


class EquipmentRequestBase(BaseModel):
    equipment_id: uuid.UUID
    description: Optional[str] = None
    request_date: datetime
    status: EquipmentRequestStatus = EquipmentRequestStatus.ACTIVE


class EquipmentRequestCreate(EquipmentRequestBase):
    pass


class EquipmentRequestUpdate(EquipmentRequestBase):
    pass


class EquipmentRequestResponse(EquipmentRequestBase):
    id: uuid.UUID
    updated_at: datetime
