from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import uuid
from app.schemas.equipment import EquipmentStatus


# TODO Update the database
class EquipmentBase(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str] = None

    # make = honda
    manufacturer: Optional[str] = None
    # model = civic
    equipment_model_number: Optional[str] = None
    # serial number = bin number of that car
    serial_number: Optional[str] = None

    in_plant_location: Optional[str] = None
    image_url: Optional[str] = None

    # Supplier information
    supplier_names: List[str] = []

    # TODO: multi-plant things

    # internal things
    status: EquipmentStatus
    created_at: datetime
    updated_at: datetime


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentResponse(EquipmentBase):
    pass


class ManyEquipmentResponse(BaseModel):
    total: int
    equipment: List[EquipmentBase]
