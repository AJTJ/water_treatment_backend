from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from app.services.database import Base
import uuid
from enum import Enum as PyEnum

if TYPE_CHECKING:
    from .equipment import Equipment


class EquipmentRequestStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class EquipmentRequest(Base):
    __tablename__ = "equipment_request"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    description = mapped_column(String, nullable=True)
    status = mapped_column(
        Enum(
            EquipmentRequestStatus,
            native_enum=False,
        ),
        default=EquipmentRequestStatus.ACTIVE,
        nullable=False,
    )
    image_url = mapped_column(String, nullable=True)
    employee_name = mapped_column(String, nullable=True)
    created_at = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
    equipment_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("equipment.id", name="fk_equipment_request_equipment_id"),
        nullable=False,
    )
    equipment: Mapped["Equipment"] = relationship(
        "Equipment", back_populates="equipment_requests"
    )
