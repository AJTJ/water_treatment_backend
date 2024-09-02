from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime, timezone

from app.schemas.equipment_request import (
    EquipmentRequest,
    EquipmentRequestStatus,
)  # SQLAlchemy model
from app.models.equipment_request import (
    EquipmentRequestCreate,
    EquipmentRequestResponse,
    EquipmentRequestUpdate,
)  # Pydantic models
from app.services.database import get_session
from app.services.google_sheets import sync_to_google_sheet

router = APIRouter()


@router.post(
    "/", response_model=EquipmentRequestResponse, status_code=status.HTTP_201_CREATED
)
def create_equipment_request(
    equipment_request: EquipmentRequestCreate, db: Session = Depends(get_session)
) -> EquipmentRequestResponse:
    db_request = EquipmentRequest(**equipment_request.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    try:
        sync_to_google_sheet(equipment_request)
    except Exception as e:
        print(f"Failed to sync to Google Sheets: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return EquipmentRequestResponse.model_validate(db_request)


@router.get("/", response_model=List[EquipmentRequestResponse])
def get_all_equipment_requests(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
) -> List[EquipmentRequestResponse]:
    requests = (
        db.query(EquipmentRequest)
        .filter(EquipmentRequest.status == EquipmentRequestStatus.ACTIVE)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [EquipmentRequestResponse.model_validate(req) for req in requests]


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

    # Update equipment request fields based on input data
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
