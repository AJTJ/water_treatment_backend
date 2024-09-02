from typing import Any, Dict, Optional
from pydantic import BaseModel
import uuid


class FailedSyncBase(BaseModel):
    equipment_request_id: uuid.UUID
    error_message: Optional[str]
    request_data: Dict[str, Any]


class FailedSyncCreate(FailedSyncBase):
    pass


class FailedSyncUpdate(FailedSyncBase):
    pass


class FailedSyncResponse(FailedSyncBase):
    pass
