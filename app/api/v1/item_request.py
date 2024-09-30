from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from tenacity import retry, stop_after_attempt, wait_exponential
from app.api.v1.item import get_item
from app.services.database_service import get_session
from app.services.google_sheets_service import sync_to_google_sheet
from app.core.logging_config import logger

# Models
from app.schemas.item_request import (
    ItemRequestCreate,
    ItemRequestResponse,
    ItemRequestUpdate,
    ItemRequestWithItemInfo,
    ManyItemRequestsResponse,
    ItemRequestBase,
)
from app.schemas.failed_sync import FailedSyncCreate

# Schemas
from app.models.failed_sync import FailedSync
from app.models.item_request import (
    ItemRequest,
    ItemRequestStatusEnum,
)


router = APIRouter()


@router.post(
    "/", response_model=ItemRequestResponse, status_code=status.HTTP_201_CREATED
)
def create_item_request(
    item_request: ItemRequestCreate,
    db: Session = Depends(get_session),
    background_tasks: BackgroundTasks = BackgroundTasks(),
) -> ItemRequestResponse:
    db_request = ItemRequest(**item_request.model_dump())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    item = get_item(item_request.item_id)

    request_and_item = ItemRequestWithItemInfo(
        **item_request.model_dump(),
        item_id=item.id,
        item_name=item.name,
    )

    try:
        sync_with_retry(request_and_item)
    except Exception as e:
        print(f"Failed to sync to Google Sheets after retries: {e}")

        failed_sync_create = FailedSyncCreate(
            item_request_id=db_request.id,
            error_message=str(e),
            request_data=request_and_item.model_dump(),
        )

        failed_sync = FailedSync(**failed_sync_create.model_dump())
        db.add(failed_sync)
        db.commit()
        # Add the background task to retry syncs
        background_tasks.add_task(retry_failed_syncs, db)

    return ItemRequestResponse.model_validate(db_request)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def sync_with_retry(request_data: ItemRequestWithItemInfo) -> None:
    sync_to_google_sheet(request_data)


def retry_failed_syncs(db: Session = Depends(get_session)) -> None:
    # Get all failed syncs
    failed_syncs: List[FailedSync] = db.query(FailedSync).all()

    for sync in failed_syncs:
        try:
            request_data: ItemRequestWithItemInfo = ItemRequestWithItemInfo(
                **sync.request_data
            )
            # Attempt to sync again
            sync_to_google_sheet(request_data)
            # If successful, remove the entry from the failed syncs table
            db.delete(sync)
            db.commit()
        except Exception as e:
            # Update the failed sync attempt count and last_attempt_at timestamp
            sync.sync_attempts += 1
            sync.last_attempt_at = func.now()
            sync.error_message = str(e)
            db.commit()
            logger.error(f"Retry sync failed for {sync.item_request_id}: {e}")


@router.get("/", response_model=ManyItemRequestsResponse)
def get_many_item_requests(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_session)
) -> ManyItemRequestsResponse:
    requests = (
        db.query(ItemRequest)
        .filter(ItemRequest.status == ItemRequestStatusEnum.ACTIVE)
        .offset(skip)
        .limit(limit)
        .all()
    )

    total = (
        db.query(ItemRequest)
        .filter(ItemRequest.status == ItemRequestStatusEnum.ACTIVE)
        .count()
    )

    return ManyItemRequestsResponse(
        total=total,
        item_requests=[ItemRequestBase.model_validate(req) for req in requests],
    )


@router.get("/{request_id}", response_model=ItemRequestResponse)
def get_item_request(
    request_id: UUID, db: Session = Depends(get_session)
) -> ItemRequestResponse:
    item_request = (
        db.query(ItemRequest)
        .filter(
            ItemRequest.id == request_id,
            ItemRequest.status == ItemRequestStatusEnum.ACTIVE,
        )
        .first()
    )
    if item_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item request not found"
        )
    return ItemRequestResponse.model_validate(item_request)


@router.put("/{request_id}", response_model=ItemRequestResponse)
def update_item_request(
    request_id: UUID,
    request_update: ItemRequestUpdate,
    db: Session = Depends(get_session),
) -> ItemRequestResponse:
    item_request = (
        db.query(ItemRequest)
        .filter(
            ItemRequest.id == request_id,
            ItemRequest.status == ItemRequestStatusEnum.ACTIVE,
        )
        .first()
    )
    if item_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item request not found"
        )

    for key, value in request_update.model_dump(exclude_unset=True).items():
        setattr(item_request, key, value)

    item_request.updated_at = func.now()  # Update the timestamp
    db.commit()
    db.refresh(item_request)
    return ItemRequestResponse.model_validate(item_request)


@router.delete("/{request_id}", response_model=ItemRequestResponse)
def delete_item_request(
    request_id: UUID, db: Session = Depends(get_session)
) -> ItemRequestResponse:
    item_request = (
        db.query(ItemRequest)
        .filter(
            ItemRequest.id == request_id,
            ItemRequest.status == ItemRequestStatusEnum.ACTIVE,
        )
        .first()
    )
    if item_request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item request not found"
        )

    item_request.status = ItemRequestStatusEnum.ARCHIVED
    db.commit()
    return ItemRequestResponse.model_validate(item_request)
