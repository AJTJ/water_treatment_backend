# app/api/v1/qr_code.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from typing import List
from uuid import UUID
from app.models.equipment import Equipment
from app.models.qr_code import QRCode, QRCodeStatus  # SQLAlchemy model
from app.schemas.qr_code import (
    QRCodeQueryParams,
    QRCodeResponseWithEquipment,
    QRCodeResponse,
    QRCodeUpdate,
)  # Pydantic models
from app.services.database_service import get_session

router = APIRouter()


@router.post(
    "/batch",
    response_model=List[QRCodeResponseWithEquipment],
    status_code=status.HTTP_201_CREATED,
)
def create_batch_qr_codes(
    number_of_qr_codes: int, db: Session = Depends(get_session)
) -> List[QRCodeResponseWithEquipment]:
    if number_of_qr_codes <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of QR codes must be positive",
        )

    # Get the current highest batch number
    max_batch_number = db.query(func.max(QRCode.batch_number)).scalar() or 0

    qr_codes: List[QRCodeResponseWithEquipment] = []
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

        qr_codes.append(QRCodeResponseWithEquipment.model_validate(qr_code))

    return qr_codes


@router.get("/", response_model=QRCodeResponse)
def get_many_qr_codes(
    query_params: QRCodeQueryParams = Depends(),
    db: Session = Depends(get_session),
) -> QRCodeResponse:

    query = db.query(QRCode).filter(QRCode.status == QRCodeStatus.ACTIVE)

    if query_params.min_batch_number is not None:
        query = query.filter(QRCode.batch_number >= query_params.min_batch_number)
    if query_params.max_batch_number is not None:
        query = query.filter(QRCode.batch_number <= query_params.max_batch_number)

    total_qr_codes = query.count()

    equipment_alias = aliased(Equipment)

    qr_codes_with_equipment = (
        query.outerjoin(equipment_alias, QRCode.equipment_id == equipment_alias.id)
        .with_entities(QRCode, equipment_alias.name.label("equipment_name"))
        .offset(query_params.skip)
        .limit(query_params.limit)
        .all()
    )

    # TODO: this needs to be tested
    qr_code_responses = [
        QRCodeResponseWithEquipment.model_validate((qr, equipment_name))
        for qr, equipment_name in qr_codes_with_equipment
    ]

    return QRCodeResponse(total=total_qr_codes, qr_codes=qr_code_responses)


@router.get("/{qr_code_id}", response_model=QRCodeResponseWithEquipment)
def get_qr_code(
    qr_code_id: UUID, db: Session = Depends(get_session)
) -> QRCodeResponseWithEquipment:
    qr_code = (
        db.query(QRCode)
        .filter(QRCode.id == qr_code_id, QRCode.status == QRCodeStatus.ACTIVE)
        .first()
    )
    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )
    return QRCodeResponseWithEquipment.model_validate(qr_code)


@router.put("/{qr_code_id}", response_model=QRCodeResponseWithEquipment)
def update_qr_code(
    qr_code_id: UUID,
    qr_code_update: QRCodeUpdate,
    db: Session = Depends(get_session),
) -> QRCodeResponseWithEquipment:
    qr_code = (
        db.query(QRCode)
        .filter(QRCode.id == qr_code_id, QRCode.status == QRCodeStatus.ACTIVE)
        .first()
    )
    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )

    # unnecessary?
    if qr_code_update.equipment_id:
        equipment = (
            db.query(Equipment)
            .filter(Equipment.id == qr_code_update.equipment_id)
            .first()
        )
        if equipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
            )

    for key, value in qr_code_update.model_dump(exclude_unset=True).items():
        setattr(qr_code, key, value)
    db.commit()
    db.refresh(qr_code)
    return QRCodeResponseWithEquipment.model_validate(qr_code)


@router.delete("/{qr_code_id}", response_model=QRCodeResponseWithEquipment)
def delete_qr_code(
    qr_code_id: UUID, db: Session = Depends(get_session)
) -> QRCodeResponseWithEquipment:
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
    return QRCodeResponseWithEquipment.model_validate(qr_code)
