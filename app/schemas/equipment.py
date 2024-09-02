import uuid
from sqlalchemy import String, ForeignKey, DateTime, Text, Enum
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from app.schemas import qr_code
from app.services.database import Base
from enum import Enum as PyEnum


class EquipmentStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Equipment(Base):
    __tablename__ = "equipment"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(String, nullable=False)
    created_at = mapped_column(
        DateTime, default=datetime.now(timezone.utc), nullable=False
    )
    updated_at = mapped_column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
    description = mapped_column(Text, nullable=True)
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

    qr_code_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("qr_code.id", name="fk_equipment_qr_code_id"),
        nullable=True,
    )

    qr_code: Mapped["qr_code.QRCode"] = relationship(
        "QRCode", back_populates="equipment"
    )
