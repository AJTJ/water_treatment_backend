import uuid
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.associations import PartRequestUrgencyLevels
from app.models.item_request import ItemRequestStatusEnum
from app.schemas.item import ItemBase, ItemBaseSimple


class PartRequest(BaseModel):
    part_id: uuid.UUID
    part: ItemBase
    quantity: int
    urgency_level: PartRequestUrgencyLevels


class ItemRequestBase(BaseModel):
    # Core Fields
    id: uuid.UUID
    description: Optional[str] = None
    image_url: Optional[str]
    requestor: Optional[str] = None

    # Associated Equipment
    item_id: Optional[uuid.UUID] = None
    item: Optional[ItemBaseSimple] = None

    # Requested Parts
    parts: Optional[List[PartRequest]] = None

    # Metadata
    status: ItemRequestStatusEnum = ItemRequestStatusEnum.ACTIVE
    created_at: datetime
    updated_at: datetime


class ItemRequestSimple(BaseModel):
    # Core Fields
    id: uuid.UUID
    description: Optional[str] = None
    image_url: Optional[str]
    requestor: Optional[str] = None

    # Associated Equipment
    item_id: Optional[uuid.UUID] = None
    # item: Optional[ItemBase] = None

    # Requested Parts
    parts: Optional[List[PartRequest]] = None

    # Metadata
    status: ItemRequestStatusEnum = ItemRequestStatusEnum.ACTIVE
    created_at: datetime
    updated_at: datetime


class ItemRequestCreate(BaseModel):
    description: Optional[str] = None
    requestor: Optional[str] = None
    image_url: Optional[str] = None
    item_id: Optional[uuid.UUID] = None
    parts: Optional[List[PartRequest]] = None


class ItemRequestUpdate(BaseModel):
    description: Optional[str] = None
    requestor: Optional[str] = None
    image_url: Optional[str]
    parts: Optional[List[PartRequest]] = None


class ItemRequestResponse(ItemRequestBase):
    pass


class ItemRequestWithItemInfo(ItemRequestBase):
    item_name: str


class ManyItemRequestsResponse(BaseModel):
    total: int
    item_requests: List[ItemRequestBase]
