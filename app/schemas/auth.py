from datetime import datetime, timezone
from sqlalchemy import String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship, Mapped
from app.services.database_service import Base
from enum import Enum as PyEnum
from typing import List


class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    SYSTEM_ADMIN = "system_admin"


class UserStatus(PyEnum):
    ACTIVE = "active"
    ARCHIVED = "archived"


class UserRoleAssociation(Base):
    __tablename__ = "user_roles"

    user_id = mapped_column(String, ForeignKey("users.id"), primary_key=True)
    role = mapped_column(
        Enum(UserRole, native_enum=False), nullable=False, primary_key=True
    )


class User(Base):
    __tablename__ = "users"
    id = mapped_column(String, nullable=False, unique=True, primary_key=True)
    user_name = mapped_column(String, nullable=False)
    email = mapped_column(String, nullable=False, unique=True)
    roles: Mapped[List[UserRoleAssociation]] = relationship(
        "UserRoleAssociation",
        backref="users",
        lazy="joined",
        collection_class=list,
        cascade="all, delete",
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
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
