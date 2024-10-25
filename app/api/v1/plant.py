from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.models.plants import Plants
from app.schemas.plant import PlantCreate, PlantResponse
from app.services.database_service import get_session

router = APIRouter()


@router.post("", response_model=PlantResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    plant: PlantCreate, db: Session = Depends(get_session)
) -> PlantResponse:
    db_plant = Plants(**plant.model_dump())
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return PlantResponse.model_validate(db_plant)
