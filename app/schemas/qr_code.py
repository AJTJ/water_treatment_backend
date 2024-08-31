from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped
from pydantic import BaseModel
from app.services.database import Base
import uuid


class QRCode(Base):
    __tablename__ = "qr_code"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_url = Column(String, nullable=False)

    equipment: Mapped["Equipment"] = relationship("Equipment", back_populates="qr_code")
