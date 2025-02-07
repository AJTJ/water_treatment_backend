from sqlalchemy import String, DateTime, JSON, Integer, func
from sqlalchemy.dialects.postgresql import UUID

from app.services.database_service import Base
from sqlalchemy.orm import mapped_column
import uuid


class FailedSyncs(Base):
    __tablename__ = "failed_syncs"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    # TODO: this should be associated correctly
    item_request_id = mapped_column(UUID(as_uuid=True), nullable=False)
    sync_attempts = mapped_column(Integer, default=0)
    last_attempt_at = mapped_column(DateTime, default=func.now())
    error_message = mapped_column(String, nullable=True)
    request_data = mapped_column(JSON, nullable=False)
