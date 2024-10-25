from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
import uuid


class SupplierBase(BaseModel):
    id: uuid.UUID
    name: str


class SupplierWithRelations(SupplierBase):
    items: Optional[list["ItemBase"]]


from app.schemas.item import ItemBase
