from typing import TYPE_CHECKING
import uuid
from sqlalchemy import Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base
from enum import Enum as PyEnum
from .associations import (
    items_item_types_association,
)

if TYPE_CHECKING:
    from app.models.items import Items


class ItemTypeEnum(PyEnum):
    EQUIPMENT = "equipment"
    PART = "part"
    CONSUMABLE = "consumable"
    TOOL = "tool"


class ItemTypes(Base):
    __tablename__ = "item_types"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(Enum(ItemTypeEnum, native_enum=False), nullable=False)

    items: Mapped[list["Items"]] = relationship(
        "Items", secondary=items_item_types_association, back_populates="item_types"
    )
