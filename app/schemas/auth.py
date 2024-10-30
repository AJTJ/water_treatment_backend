from pydantic import BaseModel
from pydantic import BaseModel


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


# LOGIN/LOGOUT
class LoginRequest(BaseModel):
    email: str
    password: str


class LogoutResponse(BaseModel):
    message: str
