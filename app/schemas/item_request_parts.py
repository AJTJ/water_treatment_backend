from typing import TYPE_CHECKING
import uuid
from pydantic import BaseModel
from app.models.associations import PartRequestUrgencyLevels


if TYPE_CHECKING:
    from app.schemas.item_and_item_request import ItemBase


class PartRequest(BaseModel):
    part_id: uuid.UUID
    part: "ItemBase"
    quantity: int
    urgency_level: PartRequestUrgencyLevels
