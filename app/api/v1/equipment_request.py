from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime, timezone
from tenacity import retry, stop_after_attempt, wait_exponential
from app.api.v1.equipment import get_equipment
from app.services.database_service import get_session
from app.services.google_sheets_service import sync_to_google_sheet
from app.core.logging_config import logger

# Models
from app.schemas.equipment_request import (
    EquipmentRequestCreate,
    EquipmentRequestResponse,
    EquipmentRequestUpdate,
    EquipmentRequestWithEquipmentInfo,
    ManyEquipmentRequestsResponse,
    EquipmentRequestBase,
)
from app.schemas.failed_sync import FailedSyncCreate

# Schemas
from app.models.failed_sync import FailedSync
from app.models.equipment_request import (
    EquipmentRequest,
    EquipmentRequestStatus,
)


router = APIRouter()


@router.post(
    "/", response_model=EquipmentRequestResponse, status_code=status.HTTP_201_CREATED
)
def create_equipment_request(
    equipment_request: EquipmentRequestCreate,
    db: Session = Depends(get_session),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> EquipmentRequestResponse:
    db_request = EquipmentRequest(**equipment_request.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    equipment = get_equipment(equipment_request.equipment_id)

    request_and_equipment = EquipmentRequestWithEquipmentInfo(
        **equipment_request.model_dump(),
        equipment_id=equipment.id,
        equipment_name=equipment.name,
    )

    try:
        sync_with_retry(request_and_equipment)
    except Exception as e:
        print(f"Failed to sync to Google Sheets after retries: {e}")

        failed_sync_create = FailedSyncCreate(
            equipment_request_id=db_request.id,
            error_message=str(e),
            request_data=request_and_equipment.model_dump(),
        )

        failed_sync = FailedSync(**failed_sync_create.model_dump())
        db.add(failed_sync)
        db.commit()
        # Add the background task to retry syncs
        background_tasks.add_task(retry_failed_syncs, db)

    return EquipmentRequestResponse.model_validate(db_request)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def sync_with_retry(request_data: EquipmentRequestWithEquipmentInfo) -> None:
    sync_to_google_sheet(request_data)


def retry_failed_syncs(db: Session = Depends(get_session)) -> None:
    # Get all failed syncs
    failed_syncs: List[FailedSync] = db.query(FailedSync).all()

    for sync in failed_syncs:
        try:
            # Attempt to deserialize request_data into EquipmentRequestWithEquipmentInfo
            request_data: EquipmentRequestWithEquipmentInfo = (
                EquipmentRequestWithEquipmentInfo(**sync.request_data)
            )
            # Attempt to sync again
            sync_to_google_sheet(request_data)
            # If successful, remove the entry from the failed syncs table
            db.delete(sync)
            db.commit()
        except Exception as e:
            # Update the failed sync attempt count and last_attempt_at timestamp
            sync.sync_attempts += 1
            sync.last_attempt_at = datetime.now(timezone.utc)
            sync.error_message = str(e)
            db.commit()
            logger.error(f"Retry sync failed for {sync.equipment_request_id}: {e}")


@router.get("/", response_model=ManyEquipmentRequestsResponse)
def get_many_equipment_requests(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
) -> ManyEquipmentRequestsResponse:
    requests = (
        db.query(EquipmentRequest)
        .filter(EquipmentRequest.status == EquipmentRequestStatus.ACTIVE)
        .offset(skip)
        .limit(limit)
        .all()
    )

    total = (
        db.query(EquipmentRequest)
        .filter(EquipmentRequest.status == EquipmentRequestStatus.ACTIVE)
        .count()
    )

    return ManyEquipmentRequestsResponse(
        total=total,
        equipment_requests=[
            EquipmentRequestBase.model_validate(req) for req in requests
        ],
    )


@router.get("/{request_id}", response_model=EquipmentRequestResponse)
def get_equipment_request(
    request_id: UUID, db: Session = Depends(get_session)
) -> EquipmentRequestResponse:
    equipment_request = (
        db.query(EquipmentRequest)
        .filter(
            EquipmentRequest.id == request_id,
            EquipmentRequest.status == EquipmentRequestStatus.ACTIVE,
        )
        .first()
    )
    if equipment_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment request not found"
        )
    return EquipmentRequestResponse.model_validate(equipment_request)


@router.put("/{request_id}", response_model=EquipmentRequestResponse)
def update_equipment_request(
    request_id: UUID,
    request_update: EquipmentRequestUpdate,
    db: Session = Depends(get_session),
) -> EquipmentRequestResponse:
    equipment_request = (
        db.query(EquipmentRequest)
        .filter(
            EquipmentRequest.id == request_id,
            EquipmentRequest.status == EquipmentRequestStatus.ACTIVE,
        )
        .first()
    )
    if equipment_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment request not found"
        )

    for key, value in request_update.model_dump(exclude_unset=True).items():
        setattr(equipment_request, key, value)

    equipment_request.updated_at = datetime.now(timezone.utc)  # Update the timestamp
    db.commit()
    db.refresh(equipment_request)
    return EquipmentRequestResponse.model_validate(equipment_request)


@router.delete("/{request_id}", response_model=EquipmentRequestResponse)
def delete_equipment_request(
    request_id: UUID, db: Session = Depends(get_session)
) -> EquipmentRequestResponse:
    equipment_request = (
        db.query(EquipmentRequest)
        .filter(
            EquipmentRequest.id == request_id,
            EquipmentRequest.status == EquipmentRequestStatus.ACTIVE,
        )
        .first()
    )
    if equipment_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment request not found"
        )

    equipment_request.status = EquipmentRequestStatus.ARCHIVED
    db.commit()
    return EquipmentRequestResponse.model_validate(equipment_request)
