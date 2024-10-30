from __future__ import annotations
import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Role(BaseModel):
    id: uuid.UUID
    name: UserRoleEnum


class UserBase(BaseModel):
    id: str
    user_name: str
    email: str

    # Metadata
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserBaseWithRelations(UserBase):
    plant_associations: Optional[list[UserPlantAssociation]]


class PlantsAndRoles(BaseModel):
    plant_id: uuid.UUID
    role: UserRoleEnum


# CREATE USER
class UserCreateRequest(BaseModel):
    user_name: str
    email: str
    global_role: UserRoleEnum
    plants_and_roles: list[PlantsAndRoles]


class UserCreateResponse(BaseModel):
    user_name: str
    email: str
    sub: str


# UPDATE USER
class UserUpdate(BaseModel):
    user_name: str
    email: str
    roles: list[UserRoleEnum]


from app.models.users import UserPlantAssociation, UserRoleEnum, UserStatus
