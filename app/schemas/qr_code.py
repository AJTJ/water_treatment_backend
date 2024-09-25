from typing import Optional
from pydantic import BaseModel
import uuid

from app.models.qr_code import QRCodeStatus


class QRCodeBase(BaseModel):
    id: uuid.UUID
    batch_number: int
    full_url: str
    status: QRCodeStatus
    equipment_id: Optional[uuid.UUID]


class QRCodeUpdate(BaseModel):
    equipment_id: Optional[uuid.UUID]


class QRCodeResponseWithEquipment(QRCodeBase):
    equipment_name: Optional[str]

    class Config:
        from_attributes = True


class QRCodeResponse(BaseModel):
    total: int
    qr_codes: list[QRCodeResponseWithEquipment]


class QRCodeQueryParams(BaseModel):
    skip: int = 0
    limit: int = 200
    min_batch_number: Optional[int] = None
    max_batch_number: Optional[int] = None
