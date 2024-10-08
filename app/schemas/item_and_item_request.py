from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Self
import uuid
from app.models.item import ItemStatusEnum
from app.models.item_type import ItemTypeEnum
from app.schemas.supplier import SupplierBaseSimple


from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.item_request import ItemRequestStatusEnum
from app.schemas.item_request_parts import PartRequest


class ItemBaseSimple(BaseModel):
    # Core Fields
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    item_types: list[ItemTypeEnum]

    # Manufacturer and Supplier information
    manufacturer: Optional[str] = None
    item_model_number: Optional[str] = None
    serial_number: Optional[str] = None
    # SIMPLE
    # suppliers: Optional[list[SupplierBaseSimple]] = None

    # Location information
    in_plant_location: Optional[str] = None
    image_url: Optional[str] = None

    # Parts (using SELF for recursive reference)
    parts: Optional[list[Self]]

    # Item Requests
    # SIMPLE
    # item_requests: Optional[list["ItemRequestBase"]] = None

    # Metadata
    status: ItemStatusEnum
    created_at: datetime
    updated_at: datetime


class ItemBase(BaseModel):

    # Core Fields
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    item_types: list[ItemTypeEnum]

    # Manufacturer and Supplier information
    manufacturer: Optional[str] = None
    item_model_number: Optional[str] = None
    serial_number: Optional[str] = None
    suppliers: Optional[list[SupplierBaseSimple]] = None

    # Location information
    in_plant_location: Optional[str] = None
    image_url: Optional[str] = None

    # Parts
    parts: Optional[list[ItemBaseSimple]]

    # Item Requests
    item_requests: Optional[list["ItemRequestBase"]] = None

    # Metadata
    status: ItemStatusEnum
    created_at: datetime
    updated_at: datetime


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class ItemResponse(ItemBase):
    pass


class ManyItemsResponse(BaseModel):
    total: int
    items: List[ItemBase]


#
#
#
#
#


class ItemRequestBase(BaseModel):
    # Core Fields
    id: uuid.UUID
    description: Optional[str] = None
    image_url: Optional[str] = None
    requestor: Optional[str] = None

    # Associated Equipment
    item_id: Optional[uuid.UUID] = None
    item: Optional["ItemBase"] = None

    # Requested Parts
    parts: Optional[List[PartRequest]] = None

    # Metadata
    status: ItemRequestStatusEnum = ItemRequestStatusEnum.ACTIVE
    created_at: datetime
    updated_at: datetime


class ItemRequestSimple(BaseModel):
    # Core Fields
    id: uuid.UUID
    description: Optional[str] = None
    image_url: Optional[str]
    requestor: Optional[str] = None

    # Associated Equipment
    item_id: Optional[uuid.UUID] = None
    # SIMPLE
    # item: Optional[ItemBase] = None

    # Requested Parts
    parts: Optional[List[PartRequest]] = None

    # Metadata
    status: ItemRequestStatusEnum = ItemRequestStatusEnum.ACTIVE
    created_at: datetime
    updated_at: datetime


class ItemRequestCreate(BaseModel):
    description: Optional[str] = None
    requestor: Optional[str] = None
    image_url: Optional[str] = None
    item_id: Optional[uuid.UUID] = None
    parts: Optional[List[PartRequest]] = None


class ItemRequestUpdate(BaseModel):
    description: Optional[str] = None
    requestor: Optional[str] = None
    image_url: Optional[str]
    parts: Optional[List[PartRequest]] = None


class ItemRequestResponse(ItemRequestBase):
    pass


class ItemRequestWithItemInfo(ItemRequestBase):
    item_name: Optional[str]


class ManyItemRequestsResponse(BaseModel):
    total: int
    item_requests: List[ItemRequestBase]
