import uuid
from sqlalchemy import String, DateTime, Text, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.services.database_service import Base
from enum import Enum as PyEnum
from .item_request import ItemRequest
from .supplier import Supplier
from .item_type import ItemType
from .associations import items_suppliers_association, items_item_types_association


class ItemStatusEnum(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Item(Base):
    __tablename__ = "item"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(String, nullable=False)
    description = mapped_column(Text, nullable=True)

    manufacturer = mapped_column(String, nullable=True)
    model_number = mapped_column(String, nullable=True)
    serial_number = mapped_column(String, nullable=True)

    in_plant_location = mapped_column(String, nullable=True)
    image_url = mapped_column(String, nullable=True)

    item_types: Mapped[list["ItemType"]] = relationship(
        "ItemType", secondary=items_item_types_association, back_populates="items"
    )

    suppliers: Mapped[list["Supplier"]] = relationship(
        "Supplier", secondary=items_suppliers_association, back_populates="items"
    )

    status = mapped_column(
        Enum(
            ItemStatusEnum,
            native_enum=False,
        ),
        default=ItemStatusEnum.ACTIVE,
        nullable=False,
    )

    created_at = mapped_column(DateTime, default=func.now(), nullable=False)

    updated_at = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    item_requests: Mapped[list["ItemRequest"]] = relationship(
        "ItemRequest", back_populates="item"
    )
