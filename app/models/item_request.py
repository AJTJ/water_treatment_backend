from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.services.database_service import Base
import uuid
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from .item import Item


class ItemRequestStatusEnum(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class ItemRequest(Base):
    __tablename__ = "item_request"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    description = mapped_column(String, nullable=True)
    status = mapped_column(
        Enum(
            ItemRequestStatusEnum,
            native_enum=False,
        ),
        default=ItemRequestStatusEnum.ACTIVE,
        nullable=False,
    )
    image_url = mapped_column(String, nullable=True)
    employee_name = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    item_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("item.id", name="fk_item_request_item_id"),
        nullable=False,
    )
    item: Mapped["Item"] = relationship("Item", back_populates="item_requests")
