import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Enum
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from app.schemas import qr_code
from app.services.database import Base
from enum import Enum as PyEnum


class EquipmentStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    status = Column(
        Enum(
            EquipmentStatus,
            native_enum=False,
        ),
        default=EquipmentStatus.ACTIVE,
        nullable=False,
    )

    qr_code_id = Column(UUID(as_uuid=True), ForeignKey("qr_code.id"), nullable=True)

    qr_code: Mapped["qr_code.QRCode"] = relationship(
        "QRCode", back_populates="equipment"
    )
