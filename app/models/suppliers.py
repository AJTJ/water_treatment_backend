from typing import TYPE_CHECKING
import uuid
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base

if TYPE_CHECKING:
    from .items import Items

from .associations import items_suppliers_association


class Suppliers(Base):
    __tablename__ = "suppliers"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(String, nullable=False)

    # Mapped implies that it is mapped to a column
    items: Mapped[list["Items"]] = relationship(
        "Items",
        secondary=items_suppliers_association,
        back_populates="suppliers",
    )
