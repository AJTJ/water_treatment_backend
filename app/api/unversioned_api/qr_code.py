from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.qr_codes import QRCodes, QRCodeStatus
from app.schemas.qr_code import (
    QRCodeResponseWithItem,
)
from app.services.database_service import get_session

router = APIRouter()


@router.get("/qr_code/{qr_code_id}", response_model=QRCodeResponseWithItem)
def handle_qr_code_scan(
    qr_code_id: UUID, db: Session = Depends(get_session)
) -> QRCodeResponseWithItem:
    qr_code = db.query(QRCodes).filter(QRCodes.id == qr_code_id).first()

    if not qr_code:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="QR Code not found"
        )

    if qr_code.status == QRCodeStatus.ARCHIVED:
        raise HTTPException(
            status_code=status.HTTP_410_GONE, detail="QR Code is archived"
        )

    return QRCodeResponseWithItem.model_validate(qr_code)
