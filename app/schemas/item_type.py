from pydantic import BaseModel
import uuid

from app.models.item_type import ItemTypeEnum


class ItemTypeBase(BaseModel):
    id: uuid.UUID
    name: ItemTypeEnum
