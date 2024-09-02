from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.services.database import Base

from app.schemas import equipment


class QRCode(Base):
    __tablename__ = "qr_code"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, nullable=False)
    batch_number = mapped_column(Integer, nullable=False)
    full_url = mapped_column(String, nullable=False)
    is_archived = mapped_column(Boolean, default=False)

    equipment_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("equipment.id"), nullable=True
    )

    equipment: Mapped["equipment.Equipment"] = relationship(
        "Equipment", back_populates="qr_code"
    )
