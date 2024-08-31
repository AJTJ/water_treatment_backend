from fastapi import FastAPI
from app.api.v1 import equipment, equipment_request
from app.services.logging_config import setup_logging

setup_logging()

app = FastAPI(title="Water Treatment API", version="1.0")

app.include_router(equipment.router, prefix="/v1/equipment", tags=["equipment"])
app.include_router(
    equipment_request.router, prefix="/v1/equipment_request", tags=["equipment_request"]
)
