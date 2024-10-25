from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base
from enum import Enum as PyEnum, auto


items_suppliers_association = Table(
    "items_suppliers_association",
    Base.metadata,
    Column(
        "item_id",
        UUID(as_uuid=True),
        ForeignKey("items.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "supplier_id",
        UUID(as_uuid=True),
        ForeignKey("suppliers.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)

items_parts_association = Table(
    "items_parts_association",
    Base.metadata,
    Column(
        "parent_item_id",
        UUID(as_uuid=True),
        ForeignKey("items.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "child_item_id",
        UUID(as_uuid=True),
        ForeignKey("items.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)

items_item_types_association = Table(
    "items_item_types",
    Base.metadata,
    Column(
        "item_id",
        UUID(as_uuid=True),
        ForeignKey("items.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "item_type_id",
        UUID(as_uuid=True),
        ForeignKey("item_types.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)


class PartRequestUrgencyLevels(PyEnum):
    urgent = auto()
    not_urgent = auto()


item_request_parts_association = Table(
    "item_request_parts",
    Base.metadata,
    Column(
        "request_id",
        UUID(as_uuid=True),
        ForeignKey("item_requests.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "part_id",
        UUID(as_uuid=True),
        ForeignKey("items.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "quantity",
        Integer,
        nullable=False,
        default=1,
    ),
    Column(
        "urgency_level",
        Enum(PartRequestUrgencyLevels, native_enum=False),
        nullable=False,
        default=PartRequestUrgencyLevels.not_urgent,
    ),
)

users_roles_association = Table(
    "users_roles_association",
    Base.metadata,
    Column(
        "user_id",
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

plants_users_association = Table(
    "plants_users_association",
    Base.metadata,
    Column(
        "plant_id",
        UUID(as_uuid=True),
        ForeignKey("plants.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
