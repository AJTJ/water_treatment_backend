import boto3
import os
from botocore.exceptions import ClientError
from fastapi import HTTPException, Response
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from mypy_boto3_cognito_idp.type_defs import (
    InitiateAuthResponseTypeDef,
    AdminCreateUserResponseTypeDef,
    GetUserResponseTypeDef,
)
from typing import Optional, Union

from app.schemas.auth import (
    CognitoLoginResponse,
    CognitoChallengeResponse,
    RefreshResponse,
)
from app.schemas.user import (
    UserCreateResponse,
)

# Correct the boto3 client initialization
cognito_client: CognitoIdentityProviderClient = boto3.client(  # type: ignore
    "cognito-idp", region_name=os.getenv("AWS_REGION")
)  # No need to type: ignore

# Fetch environment variables with fallback handling
USER_POOL_ID: Optional[str] = os.getenv("COGNITO_USER_POOL_ID")
CLIENT_ID: Optional[str] = os.getenv("COGNITO_CLIENT_ID")

# Environment variable validation
if USER_POOL_ID is None or CLIENT_ID is None:
    raise ValueError(
        "Cognito User Pool ID or Client ID not set in environment variables."
    )


def login_cognito_user(
    email: str, password: str, response: Response
) -> Union[CognitoLoginResponse, CognitoChallengeResponse]:
    try:
        if CLIENT_ID is None:
            raise ValueError("Cognito Client ID not set in environment variables.")

        print(f"LOGIN COGNITO Email: {email}, Password: {password}")

        # Call Cognito to initiate auth
        result: InitiateAuthResponseTypeDef = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )

        # Handle NEW_PASSWORD_REQUIRED challenge
        if result.get("ChallengeName") == "NEW_PASSWORD_REQUIRED":
            session: str | None = result.get("Session")
            if not session:
                raise Exception(
                    "Session token is missing in the response for new password challenge."
                )

            return CognitoChallengeResponse(
                challenge="NEW_PASSWORD_REQUIRED",
                session=session,
                message="New password required",
            )

        print(f"LOGIN COGNITO Result: {result}")

        # Extract response details
        auth_result = result.get("AuthenticationResult")
        if not auth_result:
            raise Exception("Authentication result is missing in the response")

        # Ensure critical fields are present
        access_token: Optional[str] = auth_result.get("AccessToken")
        id_token: Optional[str] = auth_result.get("IdToken")
        refresh_token: Optional[str] = auth_result.get("RefreshToken")
        token_type: Optional[str] = auth_result.get("TokenType")
        expires_in: Optional[int] = auth_result.get("ExpiresIn")

        if not all([access_token, id_token, refresh_token, token_type, expires_in]):
            raise Exception("One or more authentication fields are missing")

        # Assert to help the type checker infer that the variables are no longer None
        assert access_token is not None
        assert id_token is not None
        assert refresh_token is not None
        assert token_type is not None
        assert expires_in is not None

        user_info: GetUserResponseTypeDef = cognito_client.get_user(
            AccessToken=access_token
        )

        email_verified = False
        sub: Optional[str] = None
        attributes = user_info.get("UserAttributes")
        if attributes:
            for attribute in attributes:
                if attribute["Name"] == "email_verified":
                    email_verified = attribute.get("Value") == "true"
                    break
                if attribute["Name"] == "sub":
                    sub = attribute.get("Value")

        # Raise an exception if the email is not verified
        if not email_verified:
            raise HTTPException(
                status_code=403,
                detail="Email not verified. Please verify your email before logging in.",
            )

        if sub is None:
            raise Exception("User sub is missing in the response")

        # Set secure cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=expires_in,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=30 * 24 * 60 * 60,  # typically refresh token is valid for 30 days
        )

        # Return Pydantic model
        return CognitoLoginResponse(sub=sub)

    except cognito_client.exceptions.NotAuthorizedException as e:
        # Handle unauthorized access gracefully
        raise ClientError(
            operation_name="Login",
            error_response={"Error": {"Message": "Invalid credentials"}},
        ) from e
    except ClientError as e:
        raise Exception(f"ClientError in login: {str(e)}")
    except Exception as e:
        raise Exception(f"Error in login: {str(e)}")


def respond_to_new_password_challenge(
    email: str, new_password: str, session: str, http_response: Response
) -> CognitoLoginResponse:
    # TODO: Fix error handling
    try:
        if CLIENT_ID is None:
            raise ValueError("Cognito Client ID not set in environment variables.")
        cognito_response = cognito_client.respond_to_auth_challenge(
            ChallengeName="NEW_PASSWORD_REQUIRED",
            ClientId=CLIENT_ID,
            Session=session,
            ChallengeResponses={"USERNAME": email, "NEW_PASSWORD": new_password},
        )

        auth_result = cognito_response.get("AuthenticationResult")
        if not auth_result:
            raise HTTPException(status_code=500, detail="Failed to authenticate user")

        access_token = auth_result.get("AccessToken")
        id_token = auth_result.get("IdToken")
        refresh_token = auth_result.get("RefreshToken")
        expires_in = auth_result.get("ExpiresIn")

        if not all([access_token, id_token, refresh_token, expires_in]):
            raise HTTPException(
                status_code=500,
                detail="Incomplete authentication response from Cognito",
            )

        assert access_token is not None
        assert id_token is not None
        assert refresh_token is not None
        assert expires_in is not None

        user_info = cognito_client.get_user(AccessToken=access_token)
        sub: Optional[str] = None
        attributes = user_info.get("UserAttributes")
        if attributes:
            for attribute in attributes:
                if attribute["Name"] == "sub":
                    sub = attribute.get("Value")

        if sub is None:
            raise HTTPException(
                status_code=500, detail="User ID (sub) not found in Cognito response"
            )

        http_response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=expires_in,
        )
        http_response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=30 * 24 * 60 * 60,  # typically refresh token is valid for 30 days
        )

        return CognitoLoginResponse(sub=sub)
    except ClientError as e:
        raise Exception(f"ClientError in login: {str(e)}")
    except Exception as e:
        raise Exception(f"Error in login: {str(e)}")


# Refresh token function that returns typed Pydantic model
def refresh_user_token(refresh_token: str, response: Response) -> RefreshResponse:
    try:

        if CLIENT_ID is None:
            raise ValueError("Cognito Client ID not set in environment variables.")

        # Call Cognito to refresh token
        cognito_response: InitiateAuthResponseTypeDef = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": refresh_token},
        )

        # Extract response details
        auth_result = cognito_response.get("AuthenticationResult")
        if not auth_result:
            raise Exception("Authentication result is missing in the refresh response")

        # Ensure critical fields are present
        access_token: Optional[str] = auth_result.get("AccessToken")
        id_token: Optional[str] = auth_result.get("IdToken")
        token_type: Optional[str] = auth_result.get("TokenType")
        expires_in: Optional[int] = auth_result.get("ExpiresIn")

        if not all([access_token, id_token, token_type, expires_in]):
            raise Exception("One or more refresh token fields are missing")

        # Assert to help the type checker infer that the variables are no longer None
        assert access_token is not None
        assert id_token is not None
        assert token_type is not None
        assert expires_in is not None

        # Set secure cookies
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=expires_in,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=30 * 24 * 60 * 60,  # typically refresh token is valid for 30 days
        )

        # Return Pydantic model
        return RefreshResponse(
            access_token=access_token,
            id_token=id_token,
            token_type=token_type,
            expires_in=expires_in,
        )

    except ClientError as e:
        raise Exception(f"ClientError in refreshing token: {str(e)}")
    except Exception as e:
        raise Exception(f"Error refreshing token: {str(e)}")


# NOTE: Currently using only email based login only
def create_cognito_user(email: str) -> UserCreateResponse:
    try:
        if USER_POOL_ID is None or CLIENT_ID is None:
            raise ValueError(
                "Cognito User Pool ID or Client ID not set in environment variables."
            )

        response: AdminCreateUserResponseTypeDef = cognito_client.admin_create_user(
            UserPoolId=USER_POOL_ID,
            Username=email,
            UserAttributes=[
                {"Name": "email", "Value": email},
            ],
        )

        # Extract response details
        response_result = response.get("User")
        if not response_result:
            raise Exception("User details are missing in the response")

        _user_name: Optional[str] = response_result.get("Username")
        _email: Optional[str] = None
        _sub: Optional[str] = None
        attributes = response_result.get("Attributes")
        if attributes:
            for attribute in attributes:
                if attribute["Name"] == "email":
                    _email = attribute.get("Value")
                if attribute["Name"] == "sub":
                    _sub = attribute.get("Value")

        if not all([_user_name, _email]):
            raise Exception("One or more user creation fields are missing")

        assert _user_name is not None
        assert _email is not None
        assert _sub is not None

        return UserCreateResponse(user_name=_user_name, email=_email, sub=_sub)
    except ClientError as e:
        raise Exception(f"Error creating user: {str(e)}")


def validate_cognito_token(access_token: str) -> str:
    """Validate the access token via Cognito and return the user sub."""
    try:
        response = cognito_client.get_user(AccessToken=access_token)
        return response["Username"]  # Cognito 'sub' is returned as the Username

    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except cognito_client.exceptions.UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to validate token: {str(e)}"
        )


def global_revoke_token(token: str) -> None:
    """Revoke the refresh token."""
    try:
        cognito_client.global_sign_out(AccessToken=token)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to revoke token: {str(e)}"
        ) from e


def session_revoke_token(token: str) -> None:
    if CLIENT_ID is None:
        raise ValueError(
            "Cognito User Pool ID or Client ID not set in environment variables."
        )

    try:
        cognito_client.revoke_token(Token=token, ClientId=CLIENT_ID)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to revoke token: {str(e)}"
        ) from e


def delete_cognito_user(username: str) -> None:
    """Delete a user from Cognito."""
    try:
        if USER_POOL_ID is None:
            raise ValueError("Cognito User Pool ID not set in environment variables.")

        cognito_client.admin_delete_user(
            UserPoolId=USER_POOL_ID,
            Username=username,
        )
    except ClientError as e:
        raise Exception(f"Error deleting user: {str(e)}")
