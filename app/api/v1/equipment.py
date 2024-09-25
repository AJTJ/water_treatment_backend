from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.equipment import Equipment, EquipmentStatus
from app.schemas.equipment import (
    EquipmentBase,
    EquipmentCreate,
    EquipmentResponse,
    ManyEquipmentResponse,
    EquipmentUpdate,
)
from app.services.database_service import get_session

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


@router.get("/", response_model=ManyEquipmentResponse)
def get_many_equipment(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
) -> ManyEquipmentResponse:
    try:
        equipments = (
            db.query(Equipment)
            .filter(Equipment.status == EquipmentStatus.ACTIVE)
            .offset(skip)
            .limit(limit)
            .all()
        )
        count = (
            db.query(Equipment)
            .filter(Equipment.status == EquipmentStatus.ACTIVE)
            .count()
        )

        return ManyEquipmentResponse(
            total=count,
            equipment=[EquipmentBase.model_validate(eq) for eq in equipments],
        )

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
