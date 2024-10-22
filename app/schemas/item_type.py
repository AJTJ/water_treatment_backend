from pydantic import BaseModel
import uuid

from app.models.item_types import ItemTypeEnum


class ItemTypeBase(BaseModel):
    id: uuid.UUID
    name: ItemTypeEnum
