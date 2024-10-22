from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func
from typing import List
from uuid import UUID
from app.models.items import Items
from app.models.qr_codes import QRCodes, QRCodeStatus  # SQLAlchemy model
from app.schemas.qr_code import (
    QRCodeQueryParams,
    QRCodeResponseWithItem,
    QRCodeResponse,
    QRCodeUpdate,
)  # Pydantic models
from app.services.database_service import get_session

router = APIRouter()


@router.post(
    "/batch",
    response_model=List[QRCodeResponseWithItem],
    status_code=status.HTTP_201_CREATED,
)
def create_batch_qr_codes(
    number_of_qr_codes: int, db: Session = Depends(get_session)
) -> List[QRCodeResponseWithItem]:
    if number_of_qr_codes <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Number of QR codes must be positive",
        )

    # Get the current highest batch number
    max_batch_number = db.query(func.max(QRCodes.batch_number)).scalar() or 0

    qr_codes: List[QRCodeResponseWithItem] = []
    for i in range(number_of_qr_codes):
        new_batch_number: int = max_batch_number + 1 + i
        qr_code = QRCodes()
        qr_code.status = QRCodeStatus.ACTIVE
        db.add(qr_code)
        db.commit()
        db.refresh(qr_code)

        # TODO: Update the QR code URL to match your domain
        qr_code.full_url = f"https://yourdomain.com/qr/{qr_code.id}"
        qr_code.batch_number = new_batch_number

        db.commit()
        db.refresh(qr_code)

        qr_codes.append(QRCodeResponseWithItem.model_validate(qr_code))

    return qr_codes


@router.get("", response_model=QRCodeResponse)
def get_many_qr_codes(
    query_params: QRCodeQueryParams = Depends(),
    db: Session = Depends(get_session),
) -> QRCodeResponse:

    query = db.query(QRCodes).filter(QRCodes.status == QRCodeStatus.ACTIVE)

    if query_params.min_batch_number is not None:
        query = query.filter(QRCodes.batch_number >= query_params.min_batch_number)
    if query_params.max_batch_number is not None:
        query = query.filter(QRCodes.batch_number <= query_params.max_batch_number)

    total_qr_codes = query.count()

    item_alias = aliased(Items)

    qr_codes_with_item = (
        query.outerjoin(item_alias, QRCodes.item_id == item_alias.id)
        .with_entities(QRCodes, item_alias.name.label("item_name"))
        .offset(query_params.skip)
        .limit(query_params.limit)
        .all()
    )

    # TODO: this needs to be tested
    qr_code_responses = [
        QRCodeResponseWithItem.model_validate((qr, item_name))
        for qr, item_name in qr_codes_with_item
    ]

    return QRCodeResponse(total=total_qr_codes, qr_codes=qr_code_responses)


@router.get("/{qr_code_id}", response_model=QRCodeResponseWithItem)
def get_qr_code(
    qr_code_id: UUID, db: Session = Depends(get_session)
) -> QRCodeResponseWithItem:
    qr_code = (
        db.query(QRCodes)
        .filter(QRCodes.id == qr_code_id, QRCodes.status == QRCodeStatus.ACTIVE)
        .first()
    )
    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )
    return QRCodeResponseWithItem.model_validate(qr_code)


@router.put("/{qr_code_id}", response_model=QRCodeResponseWithItem)
def update_qr_code(
    qr_code_id: UUID,
    qr_code_update: QRCodeUpdate,
    db: Session = Depends(get_session),
) -> QRCodeResponseWithItem:
    qr_code = (
        db.query(QRCodes)
        .filter(QRCodes.id == qr_code_id, QRCodes.status == QRCodeStatus.ACTIVE)
        .first()
    )
    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )

    # unnecessary?
    if qr_code_update.item_id:
        item = db.query(Items).filter(Items.id == qr_code_update.item_id).first()
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

    for key, value in qr_code_update.model_dump(exclude_unset=True).items():
        setattr(qr_code, key, value)
    db.commit()
    db.refresh(qr_code)
    return QRCodeResponseWithItem.model_validate(qr_code)


@router.delete("/{qr_code_id}", response_model=QRCodeResponseWithItem)
def delete_qr_code(
    qr_code_id: UUID, db: Session = Depends(get_session)
) -> QRCodeResponseWithItem:
    qr_code = (
        db.query(QRCodes)
        .filter(QRCodes.id == qr_code_id, QRCodes.status == QRCodeStatus.ACTIVE)
        .first()
    )
    if qr_code is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )

    qr_code.status = QRCodeStatus.ARCHIVED
    db.commit()
    return QRCodeResponseWithItem.model_validate(qr_code)
