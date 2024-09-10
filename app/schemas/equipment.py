import uuid
from sqlalchemy import String, DateTime, Text, Enum
from datetime import datetime, timezone
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base
from enum import Enum as PyEnum
from .equipment_request import EquipmentRequest


class EquipmentStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Equipment(Base):
    __tablename__ = "equipment"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(String, nullable=False)
    description = mapped_column(Text, nullable=True)
    equipment_model_number = mapped_column(String, nullable=True)
    location = mapped_column(String, nullable=True)
    image_url = mapped_column(String, nullable=True)

    status = mapped_column(
        Enum(
            EquipmentStatus,
            native_enum=False,
        ),
        default=EquipmentStatus.ACTIVE,
        nullable=False,
    )
    created_at = mapped_column(
        DateTime, default=datetime.now(timezone.utc), nullable=False
    )
    updated_at = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )

    equipment_requests: Mapped[list["EquipmentRequest"]] = relationship(
        "EquipmentRequest", back_populates="equipment"
    )
