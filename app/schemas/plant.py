from __future__ import annotations
import uuid
from pydantic import BaseModel


class PlantBase(BaseModel):
    id: uuid.UUID
    name: str


class PlantWithRelations(PlantBase):
    items: list["ItemBase"] = []
    users: list[UserBase] = []
    qr_codes: list["QRCodeBase"] = []
    pass


class PlantCreate(BaseModel):
    name: str


class PlantResponse(PlantWithRelations):
    pass


from app.schemas.user import UserBase
from app.schemas.qr_code import QRCodeBase
from app.schemas.item import ItemBase
