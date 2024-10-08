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
from .associations import (
    items_suppliers_association,
    items_item_types_association,
    items_parts_association,
)


class ItemStatusEnum(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Item(Base):
    __tablename__ = "item"

    # Core Fields
    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(String, nullable=False)
    description = mapped_column(Text, nullable=True)
    item_types: Mapped[list["ItemType"]] = relationship(
        "ItemType", secondary=items_item_types_association, back_populates="items"
    )

    # Manufacturer and Supplier information
    manufacturer = mapped_column(String, nullable=True)
    item_model_number = mapped_column(String, nullable=True)
    serial_number = mapped_column(String, nullable=True)
    suppliers: Mapped[list["Supplier"]] = relationship(
        "Supplier", secondary=items_suppliers_association, back_populates="items"
    )

    # Location information
    in_plant_location = mapped_column(String, nullable=True)
    image_url = mapped_column(String, nullable=True)

    # Parts
    parts: Mapped[list["Item"]] = relationship(
        "Item",
        secondary=items_parts_association,
        primaryjoin=id == items_parts_association.c.parent_item_id,
        secondaryjoin=id == items_parts_association.c.child_item_id,
        backref="parents",
    )

    # Item Requests
    item_requests: Mapped[list["ItemRequest"]] = relationship(
        "ItemRequest", back_populates="item"
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
            ItemStatusEnum,
            native_enum=False,
        ),
        default=ItemStatusEnum.ACTIVE,
        nullable=False,
    )
