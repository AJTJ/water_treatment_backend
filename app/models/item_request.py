from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, DateTime, ForeignKey, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.services.database_service import Base
import uuid
from enum import Enum as PyEnum
from app.models.associations import item_request_parts_association

if TYPE_CHECKING:
    from .item import Item


class ItemRequestStatusEnum(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class ItemRequest(Base):
    __tablename__ = "item_request"

    # Core Fields
    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    description = mapped_column(String, nullable=True)
    image_url = mapped_column(String, nullable=True)
    requestor = mapped_column(String, nullable=True)

    # Associated Equipment
    item_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("item.id", name="fk_item_request_item_id"),
        nullable=True,
    )
    item: Mapped[Optional["Item"]] = relationship(
        "Item", back_populates="item_requests"
    )

    # Requested Parts
    parts: Mapped[list["Item"]] = relationship(
        "Item", secondary=item_request_parts_association
    )

    # Metadata
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    status = mapped_column(
        Enum(
            ItemRequestStatusEnum,
            native_enum=False,
        ),
        default=ItemRequestStatusEnum.ACTIVE,
        nullable=False,
    )
