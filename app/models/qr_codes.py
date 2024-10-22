from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.services.database_service import Base
from enum import Enum as PyEnum
import uuid

if TYPE_CHECKING:
    from .items import Items
    from .plants import Plants


class QRCodeStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class QRCodes(Base):
    __tablename__ = "qr_codes"

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

    # Associations
    item_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("items.id", name="fk_qr_code_item_id"),
        nullable=True,
    )

    item: Mapped["Items"] = relationship("Items")

    plant_id = mapped_column(
        UUID(as_uuid=True), ForeignKey("plants.id", ondelete="CASCADE"), nullable=False
    )

    plant: Mapped["Plants"] = relationship("Plants", back_populates="qr_codes")
