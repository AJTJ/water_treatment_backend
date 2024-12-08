from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Callable
from app.models.users import UserPlantAssociation, Users, UserRoleEnum
from app.services.auth_service import validate_cognito_token
from app.services.database_service import get_session

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_session),
) -> Users:
    """
    Retrieve the current user from the database using their Cognito access token.
    """
    access_token = credentials.credentials
    user_sub = validate_cognito_token(access_token)

    user = db.query(Users).filter(Users.id == user_sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def has_role(required_roles: List[UserRoleEnum]) -> Callable[[Users, Session], Users]:
    """
    Dependency to check if the current user has one of the specified roles for any plant.
    """

    def role_checker(
        user: Users = Depends(get_current_user),
        db: Session = Depends(get_session),
    ) -> Users:
        # Query the roles associated with the user from the UserPlantAssociation table
        roles = (
            db.query(UserPlantAssociation.role)
            .filter(UserPlantAssociation.user_id == user.id)
            .all()
        )
        user_roles = {role[0] for role in roles}  # Convert to a set of role names

        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=403,
                detail="Access forbidden: insufficient permissions",
            )
        return user

    return role_checker
