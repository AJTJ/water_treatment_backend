from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.services.database import Base
from .equipment import Equipment
import uuid


class EquipmentRequest(Base):
    __tablename__ = "equipment_request"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    request_date = mapped_column(DateTime, default=datetime.now, nullable=False)
    description = mapped_column(String, nullable=True)
    is_archived = mapped_column(Boolean, default=False)

    equipment_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("equipment.id"), nullable=False
    )

    equipment: Mapped[Equipment] = relationship(
        "Equipment", back_populates="equipment_request"
    )
