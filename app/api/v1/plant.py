from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.items import Items
from app.models.plants import Plants
from app.models.qr_codes import QRCodes
from app.models.users import UserPlantAssociation, Users
from app.schemas.plant import (
    ManyPlantsRequest,
    PlantBaseWithRelations,
    PlantCreateRequest,
    PlantUpdate,
)
from app.services.database_service import get_session

router = APIRouter()


@router.post(
    "/create",
    response_model=PlantBaseWithRelations,
    status_code=status.HTTP_201_CREATED,
)
def create_plant(
    plant_create: PlantCreateRequest, db: Session = Depends(get_session)
) -> PlantBaseWithRelations:
    try:
        # TODO: Should I be adding the System_Admin for when they create a plant?
        # if not plant_create.users:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Users are required to create a plant.",
        #     )

        new_plant: Plants = Plants(
            name=plant_create.name,
            image_url=plant_create.image_url,
            location=plant_create.location,
            requests_sheet_url=plant_create.requests_sheet_url,
        )

        db.add(new_plant)
        db.flush()

        if plant_create.users:
            for user_assignment in plant_create.users:
                db_user: Optional[Users] = (
                    db.query(Users).filter(Users.id == user_assignment.user_id).first()
                )
                if not db_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User not found: {user_assignment.user_id}",
                    )

                association = UserPlantAssociation(
                    user=db_user, plant=new_plant, role=user_assignment.role
                )
                db.add(association)

        db.commit()
        db.refresh(new_plant)
        return PlantBaseWithRelations.model_validate(new_plant)

    except HTTPException:
        db.rollback()
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        ) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e


@router.get(
    "/{plant_id}", response_model=PlantBaseWithRelations, status_code=status.HTTP_200_OK
)
def get_plant(
    plant_id: int, db: Session = Depends(get_session)
) -> PlantBaseWithRelations:
    plant = db.query(Plants).filter(Plants.id == plant_id).first()
    if not plant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found"
        )
    return PlantBaseWithRelations.model_validate(plant)


# TODO: Add security
@router.post(
    "/many", response_model=list[PlantBaseWithRelations], status_code=status.HTTP_200_OK
)
def get_many_plants(
    plant_ids: ManyPlantsRequest, db: Session = Depends(get_session)
) -> list[PlantBaseWithRelations]:
    plants = db.query(Plants).filter(Plants.id.in_(plant_ids)).all()
    if not plants:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No plants found"
        )
    return [PlantBaseWithRelations.model_validate(plant) for plant in plants]


# TODO: Add security, and better error handling
def update_plant(
    plant_id: UUID, plant_update: PlantUpdate, db: Session = Depends(get_session)
) -> PlantBaseWithRelations:
    try:
        # Retrieve the plant from the database
        db_plant: Optional[Plants] = (
            db.query(Plants).filter(Plants.id == plant_id).first()
        )
        if not db_plant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found"
            )

        # Update scalar fields
        for field in ["name", "image_url", "location", "requests_sheet_url"]:
            value = getattr(plant_update, field, None)
            if value is not None:
                setattr(db_plant, field, value)

        # Update Users
        if plant_update.users_to_add:
            for user_assignment in plant_update.users_to_add:
                db_user: Optional[Users] = (
                    db.query(Users).filter(Users.id == user_assignment.user_id).first()
                )
                if not db_user:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User not found: {user_assignment.user_id}",
                    )
                # Check if association already exists
                existing_association = (
                    db.query(UserPlantAssociation)
                    .filter_by(user_id=db_user.id, plant_id=db_plant.id)
                    .first()
                )
                if existing_association:
                    existing_association.role = user_assignment.role  # Update role
                else:
                    # Create new association
                    new_association = UserPlantAssociation(
                        user=db_user, plant=db_plant, role=user_assignment.role
                    )
                    db.add(new_association)

        # Remove Users
        if plant_update.users_to_remove:
            for user_id in plant_update.users_to_remove:
                association = (
                    db.query(UserPlantAssociation)
                    .filter_by(user_id=user_id, plant_id=db_plant.id)
                    .first()
                )
                if association:
                    db.delete(association)
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"User association not found for user_id: {user_id}",
                    )

        # Update Items
        if plant_update.items_to_add:
            items_to_add: list[Items] = (
                db.query(Items).filter(Items.id.in_(plant_update.items_to_add)).all()
            )
            found_item_ids: set[UUID] = {item.id for item in items_to_add}
            missing_item_ids: set[UUID] = (
                set(plant_update.items_to_add) - found_item_ids
            )
            if missing_item_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Items not found: {missing_item_ids}",
                )
            for item in items_to_add:
                if item not in db_plant.items:
                    db_plant.items.append(item)

        if plant_update.items_to_remove:
            items_to_remove: list[Items] = (
                db.query(Items).filter(Items.id.in_(plant_update.items_to_remove)).all()
            )
            found_item_ids_for_remove: set[UUID] = {item.id for item in items_to_remove}
            missing_item_ids_for_remove: set[UUID] = (
                set(plant_update.items_to_remove) - found_item_ids_for_remove
            )
            if missing_item_ids_for_remove:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Items not found: {missing_item_ids_for_remove}",
                )
            for item in items_to_remove:
                if item in db_plant.items:
                    db_plant.items.remove(item)

        # Update QR Codes
        if plant_update.qr_codes_to_add:
            qr_codes_to_add: list[QRCodes] = (
                db.query(QRCodes)
                .filter(QRCodes.id.in_(plant_update.qr_codes_to_add))
                .all()
            )
            found_qr_code_ids: set[UUID] = {qr_code.id for qr_code in qr_codes_to_add}
            missing_qr_code_ids: set[UUID] = (
                set(plant_update.qr_codes_to_add) - found_qr_code_ids
            )
            if missing_qr_code_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"QR codes not found: {missing_qr_code_ids}",
                )
            for qr_code in qr_codes_to_add:
                if qr_code not in db_plant.qr_codes:
                    db_plant.qr_codes.append(qr_code)

        if plant_update.qr_codes_to_remove:
            qr_codes_to_remove: list[QRCodes] = (
                db.query(QRCodes)
                .filter(QRCodes.id.in_(plant_update.qr_codes_to_remove))
                .all()
            )
            found_qr_code_ids_for_remove: set[UUID] = {
                qr_code.id for qr_code in qr_codes_to_remove
            }
            missing_qr_code_ids_for_remove: set[UUID] = (
                set(plant_update.qr_codes_to_remove) - found_qr_code_ids_for_remove
            )
            if missing_qr_code_ids_for_remove:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"QR codes not found: {missing_qr_code_ids_for_remove}",
                )
            for qr_code in qr_codes_to_remove:
                if qr_code in db_plant.qr_codes:
                    db_plant.qr_codes.remove(qr_code)

        db.commit()
        db.refresh(db_plant)
        return PlantBaseWithRelations.model_validate(db_plant)

    except HTTPException:
        # Re-raise HTTPExceptions to be handled by FastAPI
        raise
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred.",
        ) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e
