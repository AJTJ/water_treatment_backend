from .equipment import router as equipment_router
from .equipment_request import router as equipment_request_router
from .qr_code import router as qr_code_router

__all__ = ["equipment_router", "equipment_request_router", "qr_code_router"]
