from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import uuid
from app.models.item_requests import ItemRequestStatusEnum


class ItemRequestBase(BaseModel):
    # Core Fields
    id: uuid.UUID
    description: Optional[str] = None
    image_url: Optional[str] = None
    requestor: Optional[str] = None

    # Metadata
    status: ItemRequestStatusEnum = ItemRequestStatusEnum.ACTIVE
    created_at: datetime
    updated_at: datetime


class ItemRequestBaseWithRelations(ItemRequestBase):
    # Associated Equipment
    item_id: Optional[uuid.UUID] = None
    item: Optional["ItemBase"] = None

    # Requested Parts
    parts: Optional[list[PartRequestBase]] = None


class ItemRequestCreate(BaseModel):
    description: Optional[str] = None
    requestor: Optional[str] = None
    image_url: Optional[str] = None
    item_id: Optional[uuid.UUID] = None
    parts: Optional[list[PartRequestBase]] = None


class ItemRequestUpdate(BaseModel):
    description: Optional[str] = None
    requestor: Optional[str] = None
    image_url: Optional[str]
    parts: Optional[list[PartRequestBase]] = None


class ItemRequestResponse(ItemRequestBaseWithRelations):
    pass


class ItemRequestWithItemInfo(ItemRequestBaseWithRelations):
    item_name: Optional[str]


class ManyItemRequestsResponse(BaseModel):
    total: int
    item_requests: list[ItemRequestBaseWithRelations]


from app.schemas.item_request_parts import PartRequestBase
from app.schemas.item import ItemBase
