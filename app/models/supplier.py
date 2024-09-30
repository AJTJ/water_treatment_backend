from typing import TYPE_CHECKING
import uuid
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base

if TYPE_CHECKING:
    from .item import Item

# from .item import Item
from .associations import items_suppliers_association


class Supplier(Base):
    __tablename__ = "supplier"

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(String, nullable=False)

    # Mapped implies that it is mapped to a column
    item: Mapped[list["Item"]] = relationship(
        "Item",
        secondary=items_suppliers_association,
        back_populates="suppliers",
    )
