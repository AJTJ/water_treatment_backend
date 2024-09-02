from typing import Any, Dict
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build  # type: ignore
from app.models.equipment_request import (
    EquipmentRequestCreate,
)


def sync_to_google_sheet(request_data: EquipmentRequestCreate) -> None:
    # Load credentials from JSON key file
    credentials: Credentials = Credentials.from_service_account_file(
        "path/to/your/service-account-key.json",
        scopes=["https://www.googleapis.com/auth/spreadsheets"],
    )  # type: ignore

    # Initialize Google Sheets API service
    service = build("sheets", "v4", credentials=credentials)

    # Define the Google Sheet ID and the range to append data
    spreadsheet_id: str = "your_spreadsheet_id"
    range_name: str = "Sheet1!A1:D1"  # Adjust the range as necessary

    # Prepare the data to be inserted
    values: list[list[Any]] = [
        [
            str(request_data.equipment_id),
            request_data.description or "",
            request_data.request_date.isoformat(),
            request_data.status.value,
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


# request_data_example = EquipmentRequestCreate(
#     equipment_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
#     description="Replacement of filter",
#     request_date=datetime.now(),
#     status=EquipmentRequestStatus.ACTIVE,
# )

# sync_to_google_sheet(request_data_example)
