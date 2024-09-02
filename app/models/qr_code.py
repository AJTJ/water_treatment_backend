from typing import Optional
from pydantic import BaseModel
import uuid

from app.schemas.qr_code import QRCodeStatus


class QRCodeBase(BaseModel):
    id: uuid.UUID
    full_url: str
    batch_number: int
    status: QRCodeStatus = QRCodeStatus.ACTIVE


class QRCodeCreate(QRCodeBase):
    pass


class QRCodeUpdate(QRCodeBase):
    pass


class QRCodeResponse(QRCodeBase):
    id: uuid.UUID
    equipment_id: Optional[uuid.UUID] = None


class QRCodeAssociation(BaseModel):
    equipment_id: uuid.UUID
