from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated, Dict, Any
from app.models.user import User
from app.services.auth_service import cognito_client
from app.services.database_service import get_session
import jwt

# Define the OAuth2 scheme to extract the access token from the request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_session)],
) -> User:
    """
    Retrieves the authenticated user based on the provided Cognito access token.

    Args:
        token (str): The access token extracted from the request.
        db (Session): SQLAlchemy session for querying the database.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the user is not found or the token is invalid.
    """
    try:
        # Decode the access token to get the 'sub' (user ID) claim
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: User ID is missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Query the user from the database
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication error: {str(e)}",
        )


SECRET_KEY = "your-cognito-jwt-secret"
ALGORITHM = "RS256"  # Cognito typically uses RS256, adjust if necessary


def decode_access_token(token: str) -> Dict[str, Any]:
    """
    Decodes the JWT access token using Cognito's secret key.

    Args:
        token (str): The JWT token to decode.

    Returns:
        Dict[str, Any]: The decoded token payload.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
