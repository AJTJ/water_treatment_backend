from __future__ import annotations
from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class PlantBase(BaseModel):
    id: uuid.UUID
    name: str
    image_url: Optional[str]
    location: Optional[str]
    requests_sheet_url: Optional[str]

    # Metadata
    status: PlantStatus
    created_at: datetime
    updated_at: datetime


class PlantBaseWithRelations(PlantBase):
    items: list["ItemBase"]
    users_and_roles: list[UserAndRole]
    qr_codes: list["QRCodeBase"]


class PlantCreateRequest(BaseModel):
    name: str
    image_url: Optional[str]
    location: Optional[str]
    requests_sheet_url: Optional[str]
    users: Optional[list[UserRoleAssignment]]


class UserAndRole(BaseModel):
    user: "UserBase"
    role: UserRoleEnum


class UserRoleAssignment(BaseModel):
    user_id: str
    role: UserRoleEnum


class PlantUpdate(BaseModel):
    name: Optional[str]
    image_url: Optional[str]
    location: Optional[str]
    users_to_add: Optional[list[UserRoleAssignment]]
    users_to_remove: Optional[list[str]]
    items_to_add: Optional[list[uuid.UUID]]
    items_to_remove: Optional[list[uuid.UUID]]
    qr_codes_to_add: Optional[list[uuid.UUID]]
    qr_codes_to_remove: Optional[list[uuid.UUID]]


class ManyPlantsRequest(BaseModel):
    plant_ids: list[uuid.UUID]


from app.models.plants import PlantStatus
from app.schemas.qr_code import QRCodeBase
from app.schemas.item import ItemBase
from app.models.users import UserRoleEnum
from app.schemas.user import UserBase
