# app/api/v1/qr_code.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from uuid import UUID
from app.schemas.equipment import Equipment
from app.schemas.qr_code import QRCode, QRCodeStatus  # SQLAlchemy model
from app.models.qr_code import (
    QRCodeAssociation,
    QRCodeCreate,
    QRCodeResponse,
    QRCodeUpdate,
)  # Pydantic models
from app.services.database import get_session

router = APIRouter()


@router.post("/", response_model=QRCodeResponse, status_code=status.HTTP_201_CREATED)
def create_qr_code(
    qr_code: QRCodeCreate, db: Session = Depends(get_session)
) -> QRCodeResponse:
    db_qr_code = QRCode(**qr_code.model_dump())
    db.add(db_qr_code)
    db.commit()
    db.refresh(db_qr_code)
    return QRCodeResponse.model_validate(db_qr_code)


@router.post(
    "/batch", response_model=List[QRCodeResponse], status_code=status.HTTP_201_CREATED
)
def create_batch_qr_codes(
    number_of_qr_codes: int, db: Session = Depends(get_session)
) -> List[QRCodeResponse]:
    if number_of_qr_codes <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of QR codes must be positive",
        )

    # Get the current highest batch number
    max_batch_number = db.query(func.max(QRCode.batch_number)).scalar() or 0

    qr_codes: List[QRCodeResponse] = []
    for i in range(number_of_qr_codes):
        new_batch_number: int = max_batch_number + 1 + i
        qr_code = QRCode()
        qr_code.status = QRCodeStatus.ACTIVE
        db.add(qr_code)
        db.commit()
        db.refresh(qr_code)

        # TODO: Update the QR code URL to match your domain
        qr_code.full_url = f"https://yourdomain.com/qr/{qr_code.id}"
        qr_code.batch_number = new_batch_number

        db.commit()
        db.refresh(qr_code)

        qr_codes.append(QRCodeResponse.model_validate(qr_code))

    return qr_codes


@router.get("/", response_model=List[QRCodeResponse])
def get_many_qr_codes(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
) -> List[QRCodeResponse]:
    qr_codes = (
        db.query(QRCode)
        .filter(QRCode.status == QRCodeStatus.ACTIVE)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [QRCodeResponse.model_validate(qr) for qr in qr_codes]


@router.get("/{qr_code_id}", response_model=QRCodeResponse)
def get_qr_code(qr_code_id: UUID, db: Session = Depends(get_session)) -> QRCodeResponse:
    qr_code = (
        db.query(QRCode)
        .filter(QRCode.id == qr_code_id, QRCode.status == QRCodeStatus.ACTIVE)
        .first()
    )
    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )
    return QRCodeResponse.model_validate(qr_code)


@router.put("/{qr_code_id}", response_model=QRCodeResponse)
def update_qr_code(
    qr_code_id: UUID,
    qr_code_update: QRCodeUpdate,
    db: Session = Depends(get_session),
) -> QRCodeResponse:
    qr_code = (
        db.query(QRCode)
        .filter(QRCode.id == qr_code_id, QRCode.status == QRCodeStatus.ACTIVE)
        .first()
    )
    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )

    for key, value in qr_code_update.model_dump(exclude_unset=True).items():
        setattr(qr_code, key, value)
    db.commit()
    db.refresh(qr_code)
    return QRCodeResponse.model_validate(qr_code)


@router.delete("/{qr_code_id}", response_model=QRCodeResponse)
def delete_qr_code(
    qr_code_id: UUID, db: Session = Depends(get_session)
) -> QRCodeResponse:
    qr_code = (
        db.query(QRCode)
        .filter(QRCode.id == qr_code_id, QRCode.status == QRCodeStatus.ACTIVE)
        .first()
    )
    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )

    qr_code.status = QRCodeStatus.ARCHIVED
    db.commit()
    return QRCodeResponse.model_validate(qr_code)


@router.put("/{qr_code_id}/associate", response_model=QRCodeResponse)
def associate_qr_code_with_equipment(
    qr_code_id: UUID,
    association_data: QRCodeAssociation,
    db: Session = Depends(get_session),
) -> QRCodeResponse:
    # Fetch the QR code from the database
    qr_code = (
        db.query(QRCode)
        .filter(QRCode.id == qr_code_id, QRCode.status == QRCodeStatus.ACTIVE)
        .first()
    )

    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR code not found"
        )

    # Fetch the equipment from the database
    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == association_data.equipment_id)
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    # Associate the QR code with the equipment
    qr_code.equipment_id = equipment.id
    db.commit()
    db.refresh(qr_code)

    return QRCodeResponse.model_validate(qr_code)
