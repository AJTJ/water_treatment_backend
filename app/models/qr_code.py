from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.services.database_service import Base
from app.models import Item
from enum import Enum as PyEnum
import uuid


class QRCodeStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class QRCode(Base):
    __tablename__ = "qr_code"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    batch_number: Mapped[int] = mapped_column(Integer, nullable=False)
    full_url: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[QRCodeStatus] = mapped_column(
        Enum(QRCodeStatus, native_enum=False),
        default=QRCodeStatus.ACTIVE,
        nullable=False,
    )

    # ForeignKey required since this is a many-to-one relationship
    item_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("item.id", name="fk_qr_code_item_id"),
        nullable=True,
    )
    item: Mapped[Item] = relationship("Item")
