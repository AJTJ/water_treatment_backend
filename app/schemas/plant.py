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

    # Metadata
    status: PlantStatus
    created_at: datetime
    updated_at: datetime


class PlantWithRelations(PlantBase):
    items: list["ItemBase"]
    user_associations: list["UserPlantAssociation"]
    qr_codes: list["QRCodeBase"]


class PlantCreate(BaseModel):
    name: str
    image_url: Optional[str]
    location: Optional[str]
    users: list[UserRoleAssignment]


class PlantUpdate(BaseModel):
    name: Optional[str]
    image_url: Optional[str]
    location: Optional[str]
    users_to_add: list[UserRoleAssignment]
    users_to_remove: list[str]
    items_to_add: list[uuid.UUID]
    items_to_remove: list[uuid.UUID]
    qr_codes_to_add: list[uuid.UUID]
    qr_codes_to_remove: list[uuid.UUID]


class UserInPlant(BaseModel):
    user_id: str
    user_name: str
    role: UserRoleEnum


class PlantResponse(BaseModel):
    pass


class ManyPlantsRequest(BaseModel):
    plant_ids: list[uuid.UUID]


class UserRoleAssignment(BaseModel):
    user_id: str
    role: UserRoleEnum


from app.models.plants import PlantStatus
from app.schemas.qr_code import QRCodeBase
from app.schemas.item import ItemBase
from app.models.users import UserPlantAssociation, UserRoleEnum
