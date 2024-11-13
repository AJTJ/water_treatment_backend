from __future__ import annotations
from typing import Optional
import uuid
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.users import UserPlantAssociation
from app.services.database_service import Base
from enum import Enum as PyEnum
from sqlalchemy import String, DateTime, func
from sqlalchemy.types import Enum as SQLAlchemyEnum


class PlantStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class Plants(Base):
    __tablename__ = "plants"

    def __init__(
        self,
        name: str,
        image_url: Optional[str],
        location: Optional[str],
        user_associations: Optional[list["UserPlantAssociation"]] = None,
    ) -> None:
        self.name = name
        self.image_url = image_url
        self.location = location
        if user_associations is not None:
            self.user_associations = user_associations

    id = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    name = mapped_column(String, nullable=False)
    image_url = mapped_column(String, nullable=True)
    location = mapped_column(String, nullable=True)

    # Associations
    # One to many relationship with items
    user_associations: Mapped[list["UserPlantAssociation"]] = relationship(
        "UserPlantAssociation",
        back_populates="plant",
        cascade="all, delete-orphan",
    )

    items: Mapped[list["Items"]] = relationship(
        "Items",
        back_populates="plant",
        cascade="all, delete-orphan",
    )

    qr_codes: Mapped[list["QRCodes"]] = relationship(
        "QRCodes",
        back_populates="plant",
        cascade="all, delete-orphan",
    )

    # Metadata
    status = mapped_column(
        SQLAlchemyEnum(
            PlantStatus,
            native_enum=False,
        ),
        default=PlantStatus.ACTIVE,
        nullable=False,
    )

    created_at = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    model_config = {"from_attributes": True}

    # A property to access the users directly
    @property
    def users(self) -> list["Users"]:
        return [association.user for association in self.user_associations]


from app.models.items import Items
from app.models.qr_codes import QRCodes
from app.models.users import Users
