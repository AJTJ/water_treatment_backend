from sqlalchemy import String, DateTime, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.services.database import Base
from sqlalchemy.orm import mapped_column
import uuid


class FailedSync(Base):
    __tablename__ = "failed_syncs"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    equipment_request_id = mapped_column(UUID(as_uuid=True), nullable=False)
    sync_attempts = mapped_column(Integer, default=0)
    last_attempt_at = mapped_column(DateTime, default=datetime.now(timezone.utc))
    error_message = mapped_column(String, nullable=True)
    request_data = mapped_column(JSON, nullable=False)
