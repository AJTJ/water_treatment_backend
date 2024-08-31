from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime, timezone

from app.schemas.equipment import Equipment  # SQLAlchemy model
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
def read_equipments(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
) -> List[EquipmentResponse]:
    equipments = (
        db.query(Equipment)
        .filter(Equipment.is_archived == False)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [EquipmentResponse.model_validate(eq) for eq in equipments]


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def read_equipment(
    equipment_id: UUID, db: Session = Depends(get_session)
) -> EquipmentResponse:
    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == equipment_id, Equipment.is_archived == False)
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
        .filter(Equipment.id == equipment_id, Equipment.is_archived == False)
        .first()
    )
    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    for key, value in equipment_update.model_dump(exclude_unset=True).items():
        setattr(equipment, key, value)
    equipment.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(equipment)
    return EquipmentResponse.model_validate(equipment)


@router.delete("/{equipment_id}", response_model=EquipmentResponse)
def delete_equipment(
    equipment_id: UUID, db: Session = Depends(get_session)
) -> EquipmentResponse:
    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == equipment_id, Equipment.is_archived == False)
        .first()
    )
    if equipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Equipment not found"
        )

    equipment.is_archived = True
    db.commit()
    return EquipmentResponse.model_validate(equipment)
