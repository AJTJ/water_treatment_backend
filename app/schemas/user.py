from __future__ import annotations
import uuid
from pydantic import BaseModel
from datetime import datetime
from app.models.users import UserRoleEnum, UserStatus
from pydantic import BaseModel


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


class UserBaseWithRelations(UserBase):
    plants: list[PlantBase]
    roles: list[Role]


# CREATE USER
class UserCreateRequest(BaseModel):
    user_name: str
    email: str
    roles: list[UserRoleEnum]


class UserCreateResponse(BaseModel):
    user_name: str
    email: str
    sub: str


# UPDATE USER
class UserUpdate(BaseModel):
    user_name: str
    email: str
    roles: list[UserRoleEnum]


# LOGIN/LOGOUT
class LoginRequest(BaseModel):
    email: str
    password: str


class LogoutResponse(BaseModel):
    message: str


# COGNITO
class ValidTokenResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class RefreshResponse(BaseModel):
    access_token: str
    id_token: str
    token_type: str
    expires_in: int


class CognitoLoginResponse(BaseModel):
    sub: str


from app.schemas.plant import PlantBase
