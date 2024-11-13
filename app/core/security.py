from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Callable, List
from app.models.users import Users, UserRoleEnum
from app.services.auth_service import validate_cognito_token
from app.services.database_service import get_session


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_session),
) -> Users:
    access_token = credentials.credentials
    user_sub = validate_cognito_token(access_token)

    # Query the user from the database by the Cognito 'sub'
    user = db.query(Users).filter(Users.id == user_sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# This needs to be updated to check the user's roles in the UserPlantAssociation table
# def has_role(roles: List[UserRoleEnum]) -> Callable[[Users], Users]:
#     def role_checker(user: Users = Depends(get_current_user)) -> Users:

#         user_roles = {role.name for role in user.roles}
#         if not any(role in user_roles for role in roles):
#             raise HTTPException(
#                 status_code=403, detail="Access forbidden: insufficient permissions"
#             )
#         return user

#     return role_checker
