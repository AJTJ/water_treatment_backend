from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.models.user import UserRole, UserStatus


# USER ROLE ASSOCIATION
class UserRoleAssociationSchema(BaseModel):
    user_id: str
    role: UserRole


class UserBase(BaseModel):
    id: str
    user_name: str
    email: str
    roles: List[UserRole]
    status: UserStatus
    last_login: datetime


# CREATE USER
class UserCreateRequest(BaseModel):
    user_name: str
    email: str
    roles: List[UserRole]


class UserCreate(BaseModel):
    id: str
    user_name: str
    email: str
    roles: List[UserRoleAssociationSchema]


class UserCreateResponse(BaseModel):
    user_name: str
    email: str
    sub: str


# UPDATE USER
class UserUpdate(BaseModel):
    user_name: str
    email: str
    roles: List[UserRoleAssociationSchema]


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


# USER ROLES
class UserRoleAssociationBase(BaseModel):
    user_id: str
    role: UserRole


class UserRoleAssociationCreate(UserRoleAssociationBase):
    pass
