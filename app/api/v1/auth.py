from typing import Union
from fastapi import APIRouter, Depends, HTTPException, Request, Response

# from app.core.security import has_role
from app.models.plants import Plants
from app.schemas.auth import (
    ChallengeResponseRequest,
    CognitoChallengeResponse,
    LoginRequest,
    LogoutResponse,
    RefreshResponse,
)
from app.schemas.plant import PlantBase
from app.schemas.user import (
    PlantsAndRolesResponse,
    UserBase,
    UserBaseWithRelations,
    UserCreateRequest,
    UserUpdate,
)
from app.models.users import UserPlantAssociation, Users
from app.services.auth_service import (
    create_cognito_user,
    delete_cognito_user,
    login_cognito_user,
    refresh_user_token,
    respond_to_new_password_challenge,
    session_revoke_token,
)
from app.services.database_service import get_session
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/login", response_model=Union[UserBase, CognitoChallengeResponse])
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_session),
) -> Union[UserBase, CognitoChallengeResponse]:
    print("pre try")
    try:

        # Check if the user exists in the Cognito database
        cognito_response = login_cognito_user(request.email, request.password, response)

        if isinstance(cognito_response, CognitoChallengeResponse):
            return cognito_response

        print(f"Cognito Response: {cognito_response}")

        # Check if the user exists in the database using the Cognito sub
        user = db.query(Users).filter(Users.id == cognito_response.sub).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.refresh(user)
        return UserBase.model_validate(user)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/respond-to-challenge", response_model=UserBase)
def respond_to_challenge(
    request: ChallengeResponseRequest,
    response: Response,
    db: Session = Depends(get_session),
) -> UserBase:
    try:
        # Respond to the NEW_PASSWORD_REQUIRED challenge with the new password
        cognito_response = respond_to_new_password_challenge(
            request.email, request.new_password, request.session, response
        )

        # Retrieve user from the database
        user = db.query(Users).filter(Users.id == cognito_response.sub).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.refresh(user)
        return UserBase.model_validate(user)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/refresh-token", response_model=RefreshResponse)
def refresh_token(
    refresh_token: str,
    response: Response,
) -> RefreshResponse:
    return refresh_user_token(refresh_token, response)


# TEST ENDPOINT
@router.get("/user/{email}", response_model=UserBaseWithRelations)
def get_user(email: str, db: Session = Depends(get_session)) -> UserBaseWithRelations:
    try:
        user = db.query(Users).filter(Users.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        plants_and_roles = [
            PlantsAndRolesResponse(
                plant=PlantBase.model_validate(association.plant),
                role=association.role,
            )
            for association in user.plant_associations
        ]

        user_data: UserBaseWithRelations = UserBaseWithRelations(
            id=user.id,
            user_name=user.user_name,
            email=user.email,
            global_role=user.global_role,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
            plants_and_roles=plants_and_roles,
        )

        return user_data
    except Exception as e:
        print(f"Error occurred getting user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


# dependencies=[Depends(has_role([UserRoleEnum.ADMIN]))]
@router.post("/create-user")
async def create_user(
    user_create_request: UserCreateRequest,
    db: Session = Depends(get_session),
) -> UserBase:
    created_cognito_user = None
    # TODO: User is still being sent confirmation email even if the cognito user is deleted due to an error
    try:

        created_cognito_user = create_cognito_user(user_create_request.email)
        if not created_cognito_user:
            raise HTTPException(status_code=400, detail="Error creating user")

        new_user = Users(
            id=created_cognito_user.sub,
            user_name=user_create_request.user_name,
            email=user_create_request.email,
            global_role=user_create_request.global_role,
            plant_associations=[],
        )

        db.add(new_user)
        db.flush()

        plant_associations: list[UserPlantAssociation] = []

        if user_create_request.plants_and_roles:
            for plant_and_role in user_create_request.plants_and_roles:
                plant_id = plant_and_role.plant_id
                role = plant_and_role.role
                plant = db.query(Plants).filter(Plants.id == plant_id).first()
                if not plant:
                    raise HTTPException(
                        status_code=400, detail=f"Plant not found: {plant_id}"
                    )
                association = UserPlantAssociation(
                    user=new_user, plant=plant, role=role
                )
                plant_associations.append(association)

        new_user.plant_associations = plant_associations
        db.commit()

        if not new_user:
            delete_cognito_user(created_cognito_user.sub)
            raise HTTPException(status_code=404, detail="New User not found")
        return UserBase.model_validate(new_user)

    except HTTPException:
        if created_cognito_user:
            delete_cognito_user(created_cognito_user.sub)
        db.rollback()
        raise
    except Exception as e:
        print(f"Error occurred: {e}")
        if created_cognito_user:
            delete_cognito_user(created_cognito_user.sub)
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


@router.post("/update/{user_id}")
async def update_user(
    user_id: str,
    user_update_request: UserUpdate,
    db: Session = Depends(get_session),
) -> UserBase:
    try:
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user_update_request.model_dump(exclude={"roles"})
        user_data["id"] = user_id
        user = Users(**user_data)
        user.plant_associations = []

        db.add(user)
        db.commit()
        db.refresh(user, attribute_names=["roles"])

        if not user:
            raise HTTPException(status_code=404, detail="New User not found")
        return UserBase.model_validate(user)

    except Exception as e:
        print(f"Error occurred: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")
