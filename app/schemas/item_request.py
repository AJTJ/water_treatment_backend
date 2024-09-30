import uuid
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum as PyEnum

from app.models.item_request import ItemRequestStatusEnum


class UrgencyLevels(PyEnum):
    urgent = "urgent"
    not_urgent = "not_urgent"


class ItemRequestBase(BaseModel):
    id: uuid.UUID

    part_name: str
    description: Optional[str] = None
    operator_name: Optional[str] = None
    image_url: Optional[str]

    # part things
    part_number: Optional[str] = None
    quantity: Optional[int] = None
    urgency: UrgencyLevels = UrgencyLevels.not_urgent

    # internal things
    item_id: uuid.UUID
    status: ItemRequestStatusEnum = ItemRequestStatusEnum.ACTIVE
    created_at: datetime
    updated_at: datetime


class ItemRequestCreate(BaseModel):
    description: Optional[str] = None
    operator_name: Optional[str] = None
    image_url: Optional[str]
    item_id: uuid.UUID


class ItemRequestUpdate(BaseModel):
    description: Optional[str] = None
    operator_name: Optional[str] = None
    image_url: Optional[str]


class ItemRequestResponse(ItemRequestBase):
    pass


class ItemRequestWithItemInfo(ItemRequestBase):
    item_name: str


class ManyItemRequestsResponse(BaseModel):
    total: int
    item_requests: List[ItemRequestBase]
