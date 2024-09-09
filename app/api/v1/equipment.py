from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas.equipment import Equipment, EquipmentStatus  # SQLAlchemy model
from app.models.equipment import (
    EquipmentCreate,
    EquipmentResponse,
    EquipmentUpdate,
)  # Pydantic models
from app.services.database import get_session

router = APIRouter()


@router.post("/", response_model=EquipmentResponse, status_code=status.HTTP_201_CREATED)
def create_equipment(
    equipment: EquipmentCreate, db: Session = Depends(get_session)
) -> EquipmentResponse:
    db_equipment = Equipment(**equipment.model_dump())
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return EquipmentResponse.model_validate(db_equipment)


@router.get("/", response_model=List[EquipmentResponse])
def get_all_equipments(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
) -> List[EquipmentResponse]:
    print("all equipment")
    try:
        equipments = (
            db.query(Equipment)
            .filter(Equipment.status == EquipmentStatus.ACTIVE)
            .offset(skip)
            .limit(limit)
            .all()
        )
        print(equipments)
        return [EquipmentResponse.model_validate(eq) for eq in equipments]
    except Exception as e:
        print(f"Error retrieving equipment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment(
    equipment_id: UUID, db: Session = Depends(get_session)
) -> EquipmentResponse:
    equipment = (
        db.query(Equipment)
        .filter(
            Equipment.id == equipment_id, Equipment.status == EquipmentStatus.ACTIVE
        )
        .first()
    )
    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )
    return EquipmentResponse.model_validate(equipment)


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(
    equipment_id: UUID,
    equipment_update: EquipmentUpdate,
    db: Session = Depends(get_session),
) -> EquipmentResponse:

    equipment = (
        db.query(Equipment)
        .filter(
            Equipment.id == equipment_id, Equipment.status == EquipmentStatus.ACTIVE
        )
        .first()
    )
    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    for key, value in equipment_update.model_dump(exclude_unset=True).items():
        setattr(equipment, key, value)
    db.commit()
    db.refresh(equipment)
    return EquipmentResponse.model_validate(equipment)


@router.delete("/{equipment_id}", response_model=EquipmentResponse)
def delete_equipment(
    equipment_id: UUID, db: Session = Depends(get_session)
) -> EquipmentResponse:
    equipment = (
        db.query(Equipment)
        .filter(
            Equipment.id == equipment_id, Equipment.status == EquipmentStatus.ACTIVE
        )
        .first()
    )
    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    equipment.status = EquipmentStatus.ARCHIVED
    db.commit()
    return EquipmentResponse.model_validate(equipment)


# app/schemas/qr_code.py

# import uuid
# from sqlalchemy import String, Integer, Enum
# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.orm import Mapped, mapped_column, relationship
# from app.services.database import Base
# from enum import Enum as PyEnum

# class QRCodeStatus(PyEnum):
#     ACTIVE = "active"
#     ARCHIVED = "archived"

# class QRCode(Base):
#     __tablename__ = "qr_code"

#     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
#     batch_number: Mapped[int] = mapped_column(Integer, nullable=True)
#     full_url: Mapped[str] = mapped_column(String, nullable=False)
#     status: Mapped[QRCodeStatus] = mapped_column(
#         Enum(QRCodeStatus, native_enum=False),
#         default=QRCodeStatus.ACTIVE,
#         nullable=False,
#     )
#     equipment_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("equipment.id"), nullable=True)

#     equipment: Mapped["Equipment"] = relationship("Equipment", back_populates="qr_code")
