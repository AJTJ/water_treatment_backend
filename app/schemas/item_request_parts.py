from __future__ import annotations
import uuid
from pydantic import BaseModel
from app.models.associations import PartRequestUrgencyLevels


class PartRequest(BaseModel):
    part_id: uuid.UUID
    part: "ItemWithRelations"
    quantity: int
    urgency_level: PartRequestUrgencyLevels


from app.schemas.item import ItemWithRelations
