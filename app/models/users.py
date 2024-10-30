from __future__ import annotations

from sqlalchemy import UUID, ForeignKey, String, Enum, DateTime, func
from sqlalchemy.orm import mapped_column, relationship, Mapped
from app.services.database_service import Base
from enum import Enum as PyEnum
from uuid import UUID as UUIDType


class UserRoleEnum(str, PyEnum):
    SUPER_ADMIN = "SUPER_ADMIN"
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    ADMIN = "ADMIN"
    OPERATOR = "OPERATOR"


class UserStatus(str, PyEnum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class Users(Base):
    __tablename__ = "users"

    # id must be string because of the sub created by cognito
    id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, primary_key=True
    )
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    global_role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), nullable=True)

    # Associations
    plant_associations: Mapped[list["UserPlantAssociation"]] = relationship(
        "UserPlantAssociation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Metadata
    status = mapped_column(
        Enum(
            UserStatus,
            native_enum=False,
        ),
        default=UserStatus.ACTIVE,
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

    # A property to access the plant directly
    @property
    def plants(self) -> list["Plants"]:
        return [association.plant for association in self.plant_associations]


class UserPlantAssociation(Base):
    __tablename__ = "user_plant_association"

    def __init__(self, user: "Users", plant: "Plants", role: "UserRoleEnum"):
        self.user = user
        self.plant = plant
        self.role = role

    user_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), primary_key=True
    )
    plant_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True), ForeignKey("plants.id"), primary_key=True
    )
    role: Mapped[UserRoleEnum] = mapped_column(Enum(UserRoleEnum), nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="plant_associations")
    plant: Mapped["Plants"] = relationship("Plants", back_populates="user_associations")


from app.models.plants import Plants
