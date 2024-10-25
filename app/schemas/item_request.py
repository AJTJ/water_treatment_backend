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


class ItemRequestWithRelations(ItemRequestBase):
    # Associated Equipment
    item_id: Optional[uuid.UUID] = None
    item: Optional["ItemWithRelations"] = None

    # Requested Parts
    parts: Optional[list[PartRequest]] = None


class ItemRequestCreate(BaseModel):
    description: Optional[str] = None
    requestor: Optional[str] = None
    image_url: Optional[str] = None
    item_id: Optional[uuid.UUID] = None
    parts: Optional[list[PartRequest]] = None


class ItemRequestUpdate(BaseModel):
    description: Optional[str] = None
    requestor: Optional[str] = None
    image_url: Optional[str]
    parts: Optional[list[PartRequest]] = None


class ItemRequestResponse(ItemRequestWithRelations):
    pass


class ItemRequestWithItemInfo(ItemRequestWithRelations):
    item_name: Optional[str]


class ManyItemRequestsResponse(BaseModel):
    total: int
    item_requests: list[ItemRequestWithRelations]


from app.schemas.item_request_parts import PartRequest
from app.schemas.item import ItemWithRelations
