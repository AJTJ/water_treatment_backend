from typing import List
from pydantic import BaseModel
from datetime import datetime

from app.models.auth import UserRole, UserRoleAssociation, UserStatus


class User(BaseModel):
    id: str
    user_name: str
    email: str
    roles: List[UserRole]
    status: UserStatus
    last_login: datetime


class UserCreacteRequest(BaseModel):
    user_name: str
    email: str
    roles: List[UserRole]


class UserCreate(BaseModel):
    id: str
    user_name: str
    email: str
    roles: List[UserRoleAssociation]


class UserCreateResponse(BaseModel):
    user_name: str
    email: str
    sub: str


class UserUpdate(BaseModel):
    user_name: str
    email: str
    roles: List[UserRoleAssociation]


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


# User Role
class UserRoleAssociationBase(BaseModel):
    user_id: str
    role: UserRole


class UserRoleAssociationCreate(UserRoleAssociationBase):
    pass
