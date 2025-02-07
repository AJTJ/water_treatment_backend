from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.items import Items, ItemStatusEnum
from app.schemas.item import (
    ItemBaseWithRelations,
    ItemCreate,
    ItemResponse,
    ManyItemsResponse,
    ItemUpdate,
)
from app.services.database_service import get_session

router = APIRouter()


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate, db: Session = Depends(get_session)) -> ItemResponse:
    db_item = Items(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return ItemResponse.model_validate(db_item)


@router.get("", response_model=ManyItemsResponse)
def get_many_items(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
) -> ManyItemsResponse:
    try:
        items = (
            db.query(Items)
            .filter(Items.status == ItemStatusEnum.ACTIVE)
            .offset(skip)
            .limit(limit)
            .all()
        )
        count = db.query(Items).filter(Items.status == ItemStatusEnum.ACTIVE).count()

        return ManyItemsResponse(
            total=count,
            items=[ItemBaseWithRelations.model_validate(i) for i in items],
        )

    except Exception as e:
        print(f"Error retrieving item: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: UUID, db: Session = Depends(get_session)) -> ItemResponse:
    item = (
        db.query(Items)
        .filter(Items.id == item_id, Items.status == ItemStatusEnum.ACTIVE)
        .first()
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )
    return ItemResponse.model_validate(item)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: UUID,
    item_update: ItemUpdate,
    db: Session = Depends(get_session),
) -> ItemResponse:

    item = (
        db.query(Items)
        .filter(Items.id == item_id, Items.status == ItemStatusEnum.ACTIVE)
        .first()
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )

    for key, value in item_update.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return ItemResponse.model_validate(item)


@router.delete("/{item_id}", response_model=ItemResponse)
def delete_item(item_id: UUID, db: Session = Depends(get_session)) -> ItemResponse:
    item = (
        db.query(Items)
        .filter(Items.id == item_id, Items.status == ItemStatusEnum.ACTIVE)
        .first()
    )
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )

    item.status = ItemStatusEnum.ARCHIVED
    db.commit()
    return ItemResponse.model_validate(item)
