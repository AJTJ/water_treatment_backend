# app/models/__init__.py
from app.schemas.equipment import Equipment
from app.schemas.equipment_request import EquipmentRequest
from app.schemas.qr_code import QRCode, QRCodeStatus
from app.schemas.failed_sync import FailedSync
from app.schemas.auth import User, UserStatus, UserRole, UserRoleAssociation

__all__ = [
    "Equipment",
    "EquipmentRequest",
    "QRCode",
    "QRCodeStatus",
    "FailedSync",
    "User",
    "UserStatus",
    "UserRole",
    "UserRoleAssociation",
]
