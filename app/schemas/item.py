from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Self
import uuid
from app.models.items import ItemStatusEnum
from app.models.item_types import ItemTypeEnum


class ItemBase(BaseModel):
    # Core Fields
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    item_types: list[ItemTypeEnum]

    # Manufacturer and Supplier information
    manufacturer: Optional[str] = None
    item_model_number: Optional[str] = None
    serial_number: Optional[str] = None

    # Location information
    in_plant_location: Optional[str] = None
    image_url: Optional[str] = None
    plant_id: uuid.UUID

    # Parts (using SELF for recursive reference)
    parts: Optional[list[Self]]

    # Metadata
    status: ItemStatusEnum
    created_at: datetime
    updated_at: datetime


class ItemBaseWithRelations(ItemBase):
    suppliers: Optional[list["SupplierBase"]] = None
    # Item Requests
    item_requests: Optional[list["ItemRequestBase"]] = None


class ItemCreate(ItemBaseWithRelations):
    pass


class ItemUpdate(ItemBaseWithRelations):
    pass


class ItemResponse(ItemBaseWithRelations):
    pass


class ManyItemsResponse(BaseModel):
    total: int
    items: list[ItemBaseWithRelations]


from app.schemas.item_request import ItemRequestBase
from app.schemas.supplier import SupplierBase
