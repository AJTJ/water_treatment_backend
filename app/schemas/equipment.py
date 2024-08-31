import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Boolean
from datetime import datetime, timezone
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.dialects.postgresql import UUID
from app.services.database import Base
from .qr_code import QRCode


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
    is_archived = Column(Boolean, default=False)

    qr_code_id = Column(UUID(as_uuid=True), ForeignKey("qr_code.id"), nullable=True)

    qr_code: Mapped[QRCode] = relationship("QRCode", back_populates="equipment")
