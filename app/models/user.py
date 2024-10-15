import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Enum, DateTime, func
from sqlalchemy.orm import mapped_column, relationship, Mapped
from app.services.database_service import Base
from enum import Enum as PyEnum
from typing import List
from .associations import user_role_association


# Using an enum here, for now is fine, but if I require more complex roles, I will need to create a separate table
class UserRole(PyEnum):
    SUPER_ADMIN = "super_admin"
    SYSTEM_ADMIN = "system_admin"
    ADMIN = "admin"
    OPERATOR = "operator"


class UserStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class Role(Base):
    __tablename__ = "roles"

    id = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        primary_key=True,
        default=lambda: uuid.uuid4(),
    )
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    # Backref to users with this role
    users: Mapped[List["User"]] = relationship(
        "User", secondary=user_role_association, back_populates="roles"
    )

    def __init__(self, name: str) -> None:
        self.name = name


class User(Base):
    __tablename__ = "users"
    id = mapped_column(
        UUID(as_uuid=True), nullable=False, unique=True, primary_key=True
    )
    user_name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    roles: Mapped[List[Role]] = relationship(
        "Role", secondary=user_role_association, back_populates="users", lazy="joined"
    )
    status = mapped_column(
        Enum(
            UserStatus,
            native_enum=False,
        ),
        default=UserStatus.ACTIVE,
        nullable=False,
    )
    last_login = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
