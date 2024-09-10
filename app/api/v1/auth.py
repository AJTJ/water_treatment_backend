from fastapi import APIRouter, HTTPException
from app.models.auth import AuthRequest
from app.services.auth_service import (
    LoginResponse,
    RefreshResponse,
    login_user,
    refresh_user_token,
)

router = APIRouter()


@router.post("/login")
async def login(auth_request: AuthRequest) -> LoginResponse:
    try:
        tokens = login_user(auth_request.username, auth_request.password)
        return tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/refresh")
async def refresh_token(refresh_token: str) -> RefreshResponse:
    try:
        new_tokens = refresh_user_token(refresh_token)
        return new_tokens
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
