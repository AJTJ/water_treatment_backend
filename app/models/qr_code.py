from pydantic import BaseModel
import uuid


class QRCodeCreate(BaseModel):
    uuid: uuid.UUID
    full_url: str


class QRCodeResponse(BaseModel):
    uuid: uuid.UUID
    full_url: str
