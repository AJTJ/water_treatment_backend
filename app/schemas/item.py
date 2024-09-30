from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import uuid
from app.models.item import ItemStatusEnum
from app.schemas.supplier import SupplierBaseSimple


class ItemBase(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None

    # make = honda
    manufacturer: Optional[str] = None
    # model = civic
    model_number: Optional[str] = None
    # serial number = bin number of that car
    serial_number: Optional[str] = None

    in_plant_location: Optional[str] = None
    image_url: Optional[str] = None

    # Supplier information
    suppliers: Optional[list[SupplierBaseSimple]] = None

    # internal things
    status: ItemStatusEnum
    created_at: datetime
    updated_at: datetime


class ItemBaseSimple(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemResponse(ItemBase):
    pass


class ManyItemsResponse(BaseModel):
    total: int
    items: List[ItemBase]
