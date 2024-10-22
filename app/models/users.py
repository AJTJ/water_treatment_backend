import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum, DateTime, func
from sqlalchemy.orm import mapped_column, relationship, Mapped
from app.services.database_service import Base
from enum import Enum as PyEnum
from typing import TYPE_CHECKING, List
from .associations import users_roles_association, plants_users_association

if TYPE_CHECKING:
    from .plants import Plants


class UserRoleEnum(PyEnum):
    SUPER_ADMIN = "super_admin"
    SYSTEM_ADMIN = "system_admin"
    ADMIN = "admin"
    OPERATOR = "operator"


class UserStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Roles(Base):
    __tablename__ = "roles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        primary_key=True,
        default=lambda: uuid.uuid4(),
    )
    name: Mapped[UserRoleEnum] = mapped_column(
        Enum(UserRoleEnum, native_enum=False), unique=True, nullable=False
    )

    # Backref to users with this role
    users: Mapped[List["Users"]] = relationship(
        "Users", secondary=users_roles_association, back_populates="roles"
    )

    def __init__(self, name: UserRoleEnum) -> None:
        self.name = name


class Users(Base):
    __tablename__ = "users"
    # id must be string because of the sub created by cognito
    id = mapped_column(String, nullable=False, unique=True, primary_key=True)
    user_name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    roles: Mapped[List[Roles]] = relationship(
        "Roles",
        secondary=users_roles_association,
        back_populates="users",
        lazy="joined",
    )

    # Associations
    plants: Mapped[List["Plants"]] = relationship(
        "Plants",
        secondary=plants_users_association,
        back_populates="users",
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
