from typing import Optional
from pydantic import BaseModel
import uuid

from app.schemas.qr_code import QRCodeStatus


class QRCodeBase(BaseModel):
    id: uuid.UUID
    batch_number: int
    full_url: str
    status: QRCodeStatus
    equipment_id: Optional[uuid.UUID]


class QRCodeUpdate(BaseModel):
    equipment_id: Optional[uuid.UUID]


class QRCodeResponse(QRCodeBase):
    pass
