from fastapi import FastAPI, Request, Response
from app.api.v1 import equipment, equipment_request, qr_code, s3_endpoints
from app.core.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from typing import Awaitable, Dict, Callable
from fastapi.responses import JSONResponse


setup_logging()

app: FastAPI = FastAPI(title="Water Treatment API", version="1.0")


# Versioned endpoints
app.include_router(equipment.router, prefix="/v1/equipment", tags=["equipment"])
app.include_router(
    equipment_request.router, prefix="/v1/equipment_request", tags=["equipment_request"]
)
app.include_router(qr_code.router, prefix="/v1/qr_code", tags=["qr_code"])
app.include_router(s3_endpoints.router, prefix="/api/v1/s3", tags=["S3"])

# Unversioned endpoints (no prefix)
app.include_router(qr_code.router, tags=["qr_code"])

# Middleware for handling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Custom error handler for unexpected exceptions
async def add_custom_error_handling(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    try:
        response: Response = await call_next(request)
        return response
    except Exception as _exc:
        # Log the error or send it to an error tracking system
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error"},
        )


app.middleware("http")(add_custom_error_handling)


# Health check endpoint
@app.get("/health", tags=["system"])
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}
