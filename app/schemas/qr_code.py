from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from app.services.database import Base

from app.schemas import equipment


class QRCode(Base):
    __tablename__ = "qr_code"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False)
    batch_number = Column(Integer, nullable=False)
    full_url = Column(String, nullable=False)
    is_archived = Column(Boolean, default=False)

    equipment_id = Column(UUID(as_uuid=True), ForeignKey("equipment.id"), nullable=True)

    equipment: Mapped["equipment.Equipment"] = relationship(
        "Equipment", back_populates="qr_code"
    )
