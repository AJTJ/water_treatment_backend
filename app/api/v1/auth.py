from fastapi import APIRouter, Depends, HTTPException, Response
from app.schemas.auth import (
    LogoutResponse,
    UserCreacteRequest,
    UserCreate,
    LoginRequest,
    RefreshResponse,
    UserRoleAssociationCreate,
)
from app.models.auth import User, UserRoleAssociation
from app.services.auth_service import (
    create_cognito_user,
    login_cognito_user,
    refresh_user_token,
)
from app.services.database_service import get_session
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login", response_model=User)
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_session),
) -> User:
    # Check if the user exists in the complementary database
    cognito_response = login_cognito_user(request.email, request.password, response)

    # Check if the user exists in the complementary database using the Cognito sub
    user = db.query(User).filter(User.id == cognito_response.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.refresh(user)
    return user


@router.post("/refresh-token", response_model=RefreshResponse)
def refresh_token(
    refresh_token: str,
    response: Response,
) -> RefreshResponse:
    return refresh_user_token(refresh_token, response)


@router.post("/create-user/")
async def create_user_endpoint(
    user_create_request: UserCreacteRequest,
    db: Session = Depends(get_session),
) -> User:
    response = create_cognito_user(
        user_create_request.user_name, user_create_request.email
    )
    if not response:
        raise HTTPException(status_code=400, detail="Error creating user")

    roles_associations = [
        UserRoleAssociationCreate(user_id=response.sub, role=role)
        for role in user_create_request.roles
    ]

    roles = [UserRoleAssociation(**role.model_dump()) for role in roles_associations]

    user_create = UserCreate(
        id=response.sub,
        user_name=user_create_request.user_name,
        email=user_create_request.email,
        roles=roles,
    )

    user = User(**user_create.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)

    if not user:
        raise HTTPException(status_code=404, detail="New User not found")
    return user


@router.post("/logout/")
async def logout(response: Response) -> LogoutResponse:
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return LogoutResponse(message="Logged out successfully")


# @router.put("/update-user/{user_id}")
# def update_user(
#     user_id: str,
#     user_update_request: UserUpdateRequest,
#     db: Session = Depends(get_session),
# ) -> User:
#     # Check if the user exists
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Update the user's attributes
#     user.user_name = user_update_request.user_name
#     user.email = user_update_request.email

#     # Update the user's roles
#     roles_associations = [
#         UserRoleAssociationCreate(user_id=user_id, role=role)
#         for role in user_update_request.roles
#     ]
#     roles = [UserRoleAssociation(**role.model_dump()) for role in roles_associations]
#     user.roles = roles

#     db.commit()
#     db.refresh(user)

#     return user
