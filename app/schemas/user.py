from __future__ import annotations
import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from app.schemas.plant import PlantBase


class UserBase(BaseModel):
    id: str
    user_name: str
    email: str
    global_role: Optional[UserRoleEnum]

    # Metadata
    status: UserStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlantsAndRolesResponse(BaseModel):
    plant: PlantBase
    role: UserRoleEnum


class UserBaseWithRelations(UserBase):
    plants_and_roles: Optional[list[PlantsAndRolesResponse]]


class PlantsAndRolesCreation(BaseModel):
    plant_id: uuid.UUID
    role: UserRoleEnum


# CREATE USER
class UserCreateRequest(BaseModel):
    user_name: str
    email: str
    global_role: UserRoleEnum
    plants_and_roles: list[PlantsAndRolesCreation]


class UserCreateResponse(BaseModel):
    user_name: str
    email: str
    sub: str


# UPDATE USER
class UserUpdate(BaseModel):
    user_name: str
    email: str
    global_role: UserRoleEnum
    plants_and_roles: Optional[list[PlantsAndRolesCreation]]


from app.models.users import UserRoleEnum, UserStatus
