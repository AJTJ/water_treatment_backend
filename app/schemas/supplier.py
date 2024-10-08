from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel
import uuid

if TYPE_CHECKING:
    from app.schemas.item_and_item_request import ItemBaseSimple


class SupplierBase(BaseModel):
    id: uuid.UUID
    name: str
    items: Optional[list["ItemBaseSimple"]]


class SupplierBaseSimple(BaseModel):
    id: uuid.UUID
    name: str
