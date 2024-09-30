from typing import Optional
from pydantic import BaseModel
import uuid
from app.schemas.item import ItemBaseSimple


class SupplierBase(BaseModel):
    id: uuid.UUID
    name: str
    items: Optional[list[ItemBaseSimple]]


class SupplierBaseSimple(BaseModel):
    id: uuid.UUID
    name: str
