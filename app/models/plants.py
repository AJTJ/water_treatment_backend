from typing import TYPE_CHECKING
import uuid
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base
from .associations import plants_users_association

if TYPE_CHECKING:
    from .items import Items
    from .users import Users
    from .qr_codes import QRCodes


class Plants(Base):
    __tablename__ = "plants"

    def __init__(self, name: str) -> None:
        self.name = name

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(String, nullable=False)

    # Associations
    # One to many relationship with items
    items: Mapped[list["Items"]] = relationship(
        "Items",
        back_populates="plant",
        cascade="all, delete-orphan",
    )

    # Many to many relationship with users
    users: Mapped[list["Users"]] = relationship(
        "Users",
        secondary=plants_users_association,
        back_populates="plants",
    )

    # One to many relationship with qr_codes
    qr_codes: Mapped[list["QRCodes"]] = relationship(
        "QRCodes",
        back_populates="plant",
        cascade="all, delete-orphan",
    )
