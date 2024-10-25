import os  # Add import statement for os module

from typing import Any
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

from googleapiclient.discovery import build  # type: ignore

# from uuid import UUID
from datetime import datetime
import pytz

from app.schemas.item_request import ItemRequestWithItemInfo


def format_date(request_date: datetime, timezone: str = "America/Whitehorse") -> str:
    local_tz = pytz.timezone(timezone)
    localized_date: datetime = request_date.astimezone(local_tz)
    return localized_date.strftime("%Y-%m-%d %H:%M:%S")


# Load environment variables from .env file (only for local dev)
load_dotenv()

# Get the path to the service account JSON file from environment variables
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS", "")


def sync_to_google_sheet(request_data: ItemRequestWithItemInfo) -> None:
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

    formatted_date = format_date(request_data.created_at, timezone="America/Whitehorse")

    values: list[list[str]] = [
        [
            formatted_date,
            request_data.item_name or "",
            request_data.description or "",
            request_data.image_url or "",
            str(request_data.id),
            str(request_data.item_id),
        ]
    ]

    body: dict[str, Any] = {"majorDimension": "ROWS", "values": values}

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
