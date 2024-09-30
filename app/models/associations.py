from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from app.services.database_service import Base


items_suppliers_association = Table(
    "items_suppliers",
    Base.metadata,
    Column(
        "item_id",
        UUID(as_uuid=True),
        ForeignKey("item.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "supplier_id",
        UUID(as_uuid=True),
        ForeignKey("supplier.id"),
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
        ForeignKey("item.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "child_item_id",
        UUID(as_uuid=True),
        ForeignKey("item.id"),
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
        ForeignKey("item.id"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "item_type_id",
        UUID(as_uuid=True),
        ForeignKey("item_type.id"),
        primary_key=True,
        nullable=False,
    ),
)
