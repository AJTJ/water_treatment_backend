import os  # Add import statement for os module

from typing import Any, Dict
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build  # type: ignore
from app.models.equipment_request import (
    EquipmentRequestWithEquipmentInfo,
)
from uuid import UUID
from datetime import datetime
import pytz


def format_date(request_date: datetime, timezone: str = "America/Whitehorse") -> str:
    local_tz = pytz.timezone(timezone)
    localized_date: datetime = request_date.astimezone(local_tz)
    return localized_date.strftime("%Y-%m-%d %H:%M:%S")


# Load environment variables from .env file (only for local dev)
load_dotenv()

# Get the path to the service account JSON file from environment variables
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "")


def sync_to_google_sheet(request_data: EquipmentRequestWithEquipmentInfo) -> None:
    # Load credentials from JSON key file
    credentials: Credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )  # type: ignore

    # Initialize Google Sheets API service
    service: Any = build("sheets", "v4", credentials=credentials)

    # Define the Google Sheet ID and the range to append data
    spreadsheet_id: str = "1FN2Ua__1dRYFCtMvBX2n-qwKIzyXWAq1dii5CmIPUrM"
    range_name: str = "Sheet1!A1:D1"  # Adjust the range as necessary

    formatted_date = format_date(
        request_data.request_date, timezone="America/Whitehorse"
    )

    values: list[list[str]] = [
        [
            request_data.equipment_name,
            request_data.description or "",
            formatted_date,
            request_data.image_url or "",
            str(request_data.id),
            str(request_data.equipment_id),
        ]
    ]

    body: Dict[str, Any] = {"majorDimension": "ROWS", "values": values}

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body,  # type: ignore
        )
        .execute()
    )

    updated_cells = result.get("updates", {}).get("updatedCells", 0)
    print(f"{updated_cells} cells updated.")


request_data_example = EquipmentRequestWithEquipmentInfo(
    request_date=datetime.now(),
    equipment_name="Filter system",
    description="Need new filter cartridges",
    image_url="https://example.com/image.jpg",
    id=UUID("123e4567-e89b-12d3-a456-426614174000"),
    equipment_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
)

sync_to_google_sheet(request_data_example)

# TODO Upload the json file to EC2

# Deployment on EC2:
# Move the JSON file to a secure directory on the EC2 instance, such as /etc/myapp/.

# Set the environment variable on the EC2 instance:

# You can set environment variables using different methods:

# Using EC2 User Data: You can add commands to the EC2 instance launch script to set the environment variable.

# bash
# Copy code
# export GOOGLE_SHEETS_CREDENTIALS=/etc/myapp/google_sheets_key.json
# Using AWS Systems Manager Parameter Store: Store the file path as a parameter and retrieve it at runtime.

# Using AWS Secrets Manager: If the file contains sensitive information, consider using AWS Secrets Manager to store and retrieve it securely.

# Modify your application startup script or deployment scripts to ensure the environment variable is set correctly before the application starts.

# 6. Security Considerations:
# Permissions: Ensure that the JSON file has restricted permissions (chmod 600 /etc/myapp/google_sheets_key.json) so that only the application user can read it.
# Environment Variable Management: Use tools like AWS Secrets Manager, SSM Parameter Store, or Docker secrets to manage sensitive environment variables securely.
# Environment Isolation: Use different credentials for different environments (development, staging, production) to minimize the risk of accidental data exposure.
