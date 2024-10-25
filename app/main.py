from fastapi import FastAPI, Request, Response
from app.api.v1 import auth, item, item_request, plant, qr_code, s3_endpoints
from app.api.unversioned_api import qr_code as qr_code_unversioned
from app.core.logging_config import setup_logging
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Awaitable, Callable
from fastapi.responses import JSONResponse


setup_logging()

app: FastAPI = FastAPI(title="Water Treatment API", version="1.0")

# Middleware for handling CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     "http://localhost:3000"
    # ],  # Change this to specific domains in production
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.options("/{rest_of_path:path}")
async def preflight_handler(response: Response) -> Response:
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


# Versioned endpoints
app.include_router(item.router, prefix="/v1/item", tags=["item"])
app.include_router(
    item_request.router, prefix="/v1/item_request", tags=["item_request"]
)
app.include_router(qr_code.router, prefix="/v1/qr_code", tags=["qr_code"])
app.include_router(s3_endpoints.router, prefix="/api/v1/s3", tags=["S3"])
app.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
app.include_router(plant.router, prefix="/v1/plant", tags=["plant"])

# Unversioned endpoints (no prefix)
app.include_router(qr_code_unversioned.router, tags=["qr_code_unversioned"])


@app.middleware("http")
async def log_request_data(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Any:
    print(f"Request URL: {request.url.path}")
    response: Any = await call_next(request)
    return response


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
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
