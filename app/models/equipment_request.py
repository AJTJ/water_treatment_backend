from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.equipment import Equipment
from app.services.database import Base


class EquipmentRequest(Base):
    __tablename__ = "equipment_request"

    id = Column(Integer, primary_key=True, index=True)
    equipment_id = Column(Integer, ForeignKey("equipment.id"), nullable=False)
    request_date = Column(DateTime, default=datetime.now, nullable=False)
    description = Column(String, nullable=True)

    equipment: Mapped["Equipment"] = relationship(
        "Equipment", back_populates="equipment_request"
    )


# Pydantic model for validation
class EquipmentRequestCreate(BaseModel):
    equipment_id: int
    description: Optional[str] = None
