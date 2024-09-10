import boto3
import os
from botocore.exceptions import ClientError
from mypy_boto3_cognito_idp import CognitoIdentityProviderClient
from mypy_boto3_cognito_idp.type_defs import InitiateAuthResponseTypeDef
from typing import Optional
from pydantic import BaseModel

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


class LoginResponse(BaseModel):
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


# Login function that returns typed Pydantic model
def login_user(username: str, password: str) -> LoginResponse:
    try:

        if CLIENT_ID is None:
            raise ValueError("Cognito Client ID not set in environment variables.")

        # Call Cognito to initiate auth
        response: InitiateAuthResponseTypeDef = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": username, "PASSWORD": password},
        )

        # Extract response details
        auth_result = response.get("AuthenticationResult")
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

        # Return Pydantic model
        return LoginResponse(
            access_token=access_token,
            id_token=id_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_in=expires_in,
        )

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


# Refresh token function that returns typed Pydantic model
def refresh_user_token(refresh_token: str) -> RefreshResponse:
    try:

        if CLIENT_ID is None:
            raise ValueError("Cognito Client ID not set in environment variables.")

        # Call Cognito to refresh token
        response: InitiateAuthResponseTypeDef = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow="REFRESH_TOKEN_AUTH",
            AuthParameters={"REFRESH_TOKEN": refresh_token},
        )

        # Extract response details
        auth_result = response.get("AuthenticationResult")
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
