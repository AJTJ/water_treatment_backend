from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from datetime import datetime
from app.services.database import Base
from .equipment import Equipment
import uuid


class EquipmentRequest(Base):
    __tablename__ = "equipment_request"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    request_date = Column(DateTime, default=datetime.now, nullable=False)
    description = Column(String, nullable=True)
    is_archived = Column(Boolean, default=False)

    equipment_id = Column(
        UUID(as_uuid=True), ForeignKey("equipment.id"), nullable=False
    )

    equipment: Mapped[Equipment] = relationship(
        "Equipment", back_populates="equipment_request"
    )
