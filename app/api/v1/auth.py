from fastapi import APIRouter, Depends, HTTPException, Request, Response

# from app.core.security import has_role
from app.schemas.user import (
    LogoutResponse,
    UserBase,
    UserCreateRequest,
    LoginRequest,
    RefreshResponse,
)
from app.models.users import Roles, Users
from app.services.auth_service import (
    create_cognito_user,
    login_cognito_user,
    refresh_user_token,
    session_revoke_token,
)
from app.services.database_service import get_session
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", response_model=UserBase)
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_session),
) -> UserBase:
    # Check if the user exists in the complementary database
    cognito_response = login_cognito_user(request.email, request.password, response)

    # Check if the user exists in the complementary database using the Cognito sub
    user = db.query(Users).filter(Users.id == cognito_response.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.refresh(user)
    return UserBase.model_validate(user)


@router.post("/refresh-token", response_model=RefreshResponse)
def refresh_token(
    refresh_token: str,
    response: Response,
) -> RefreshResponse:
    return refresh_user_token(refresh_token, response)


# dependencies=[Depends(has_role([UserRoleEnum.ADMIN]))]
@router.post("/create-user")
async def create_user(
    user_create_request: UserCreateRequest,
    db: Session = Depends(get_session),
) -> UserBase:
    try:
        print(f"Request Data: {user_create_request}")  # Log incoming data

        created_cognito_user = create_cognito_user(user_create_request.email)
        if not created_cognito_user:
            raise HTTPException(status_code=400, detail="Error creating user")

        request_roles = [role.value for role in user_create_request.roles]

        roles = db.query(Roles).filter(Roles.name.in_(request_roles)).all()

        if not roles:
            raise HTTPException(status_code=404, detail="Invalid roles provided")

        user_data = user_create_request.model_dump()
        user_data["id"] = created_cognito_user.sub
        user = Users(**user_data)
        user.roles = roles

        db.add(user)
        db.commit()
        db.refresh(user)

        if not user:
            raise HTTPException(status_code=404, detail="New User not found")
        return UserBase.model_validate(user)

    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/logout")
async def logout(request: Request, response: Response) -> LogoutResponse:
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="No refresh token provided")

    session_revoke_token(refresh_token)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return LogoutResponse(message="Logged out successfully")
