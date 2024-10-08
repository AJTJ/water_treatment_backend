from sqlalchemy import Column, Enum, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base
from enum import Enum as PyEnum


items_suppliers_association = Table(
    "items_suppliers",
    Base.metadata,
    Column(
        "item_id",
        UUID(as_uuid=True),
        ForeignKey("item.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "supplier_id",
        UUID(as_uuid=True),
        ForeignKey("supplier.id", ondelete="CASCADE"),
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
        ForeignKey("item.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "child_item_id",
        UUID(as_uuid=True),
        ForeignKey("item.id", ondelete="CASCADE"),
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
        ForeignKey("item.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "item_type_id",
        UUID(as_uuid=True),
        ForeignKey("item_type.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)


class PartRequestUrgencyLevels(PyEnum):
    urgent = "urgent"
    not_urgent = "not_urgent"


item_request_parts_association = Table(
    "item_request_parts",
    Base.metadata,
    Column(
        "request_id",
        UUID(as_uuid=True),
        ForeignKey("item_request.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "part_id",
        UUID(as_uuid=True),
        ForeignKey("item.id", ondelete="CASCADE"),
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
