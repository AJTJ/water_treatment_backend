from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from app.services.database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    qr_code_link = Column(String, nullable=True)


class EquipmentCreate(BaseModel):
    name: str
    qr_code_link: str
