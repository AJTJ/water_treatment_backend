from typing import Optional
from pydantic import BaseModel
import uuid


class QRCodeBase(BaseModel):
    id: uuid.UUID
    full_url: str
    batch_number: Optional[int] = None
    equipment_id: Optional[uuid.UUID] = None


class QRCodeCreate(QRCodeBase):
    pass


class QRCodeUpdate(QRCodeBase):
    pass


class QRCodeResponse(QRCodeBase):
    id: uuid.UUID
