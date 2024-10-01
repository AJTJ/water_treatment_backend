from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import uuid
from app.models.item import ItemStatusEnum
from app.models.item_type import ItemTypeEnum
from app.schemas.item_request import ItemRequestBase
from app.schemas.supplier import SupplierBaseSimple

# Notes
# manufacturer (make) = honda
# model = civic
# serial number = bin number of that car


class ItemBaseSimple(BaseModel):
    # Core Fields
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    item_types: list[ItemTypeEnum]

    # Manufacturer and Supplier information
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    # suppliers: Optional[list[SupplierBaseSimple]] = None

    # Location information
    in_plant_location: Optional[str] = None
    image_url: Optional[str] = None

    # Parts
    # parts: Optional[list[Self]]

    # Item Requests
    # item_requests: Optional[list[ItemRequestBase]] = None

    # Metadata
    status: ItemStatusEnum
    created_at: datetime
    updated_at: datetime


class ItemBase(BaseModel):
    # Core Fields
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    item_types: list[ItemTypeEnum]

    # Manufacturer and Supplier information
    manufacturer: Optional[str] = None
    model_number: Optional[str] = None
    serial_number: Optional[str] = None
    suppliers: Optional[list[SupplierBaseSimple]] = None

    # Location information
    in_plant_location: Optional[str] = None
    image_url: Optional[str] = None

    # Parts
    parts: Optional[list[ItemBaseSimple]]

    # Item Requests
    item_requests: Optional[list[ItemRequestBase]] = None

    # Metadata
    status: ItemStatusEnum
    created_at: datetime
    updated_at: datetime


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemResponse(ItemBase):
    pass


class ManyItemsResponse(BaseModel):
    total: int
    items: List[ItemBase]
