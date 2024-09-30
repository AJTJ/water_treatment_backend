import uuid
from sqlalchemy import Enum
from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base
from enum import Enum as PyEnum


class ItemTypeEnum(PyEnum):
    EQUIPMENT = "equipment"
    PART = "part"
    CONSUMABLE = "consumable"
    TOOL = "tool"


class ItemType(Base):
    __tablename__ = "item_type"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(Enum(ItemTypeEnum, native_enum=False), nullable=False)
