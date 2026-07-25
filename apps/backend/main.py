"""
main.py — FastAPI Application Bootstrap
=========================================
Entry point for the Digital Product Marketplace backend API.
Registers all middleware, routers, exception handlers, and lifecycle events.

Reusable pattern: This bootstrap pattern can be copied to any FastAPI project.
Add new routers under `app.include_router(...)`.
"""

import uuid
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.database.session import engine

logger = get_logger(__name__)


# ── Sentry Error Tracking (Production Only) ───────────────────
if settings.SENTRY_DSN and settings.ENVIRONMENT == "production":
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=0.2,  # 20% performance traces
        integrations=[
            StarletteIntegration(transaction_style="endpoint"),
            FastApiIntegration(),
        ],
    )


# ── Application Lifespan ──────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Startup and shutdown lifecycle manager.
    Reusable pattern: Add DB pool initialization and graceful shutdown here.
    """
    logger.info(
        "🚀 Starting Digital Product Marketplace API",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )
    # Startup: Connection pools initialize lazily via SQLAlchemy AsyncEngine
    yield
    # Shutdown: Dispose DB connection pool gracefully
    await engine.dispose()
    logger.info("🛑 API server shut down gracefully")


# ── FastAPI Application Instance ──────────────────────────────
def create_application() -> FastAPI:
    """
    Application factory pattern.
    Reusable pattern: Instantiate the app here for testability.
    """
    application = FastAPI(
        title=settings.APP_NAME,
        description="Enterprise-grade Digital Product Marketplace REST API",
        version=settings.APP_VERSION,
        docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
        redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
        openapi_url="/api/openapi.json" if settings.ENVIRONMENT != "production" else None,
        lifespan=lifespan,
    )

    # ── CORS Middleware ────────────────────────────────────────
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,  # Required for HttpOnly refresh cookie
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Request-Id", "X-RateLimit-Limit", "X-RateLimit-Remaining"],
    )

    # ── Register API Routers ───────────────────────────────────
    application.include_router(api_v1_router, prefix="/api/v1")

    return application


app = create_application()


# ── Global Exception Handlers ─────────────────────────────────

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Transforms Pydantic validation errors into the standardized RFC 7807
    error response format consumed by the frontend.
    """
    trace_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    details = [
        {
            "field": ".".join(str(loc) for loc in error["loc"] if loc != "body"),
            "reason": error["msg"],
        }
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_FAILED",
                "message": "The request payload failed schema validation.",
                "details": details,
                "traceId": trace_id,
            },
            "meta": {
                "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
                "path": str(request.url.path),
                "method": request.method,
            },
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    """Catch-all handler for unhandled server errors — prevents leaking stack traces."""
    trace_id = request.headers.get("X-Request-Id", str(uuid.uuid4()))
    logger.exception("Unhandled exception", exc_info=exc, trace_id=trace_id)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
                "traceId": trace_id,
            },
            "meta": {
                "timestamp": __import__("datetime").datetime.utcnow().isoformat() + "Z",
                "path": str(request.url.path),
                "method": request.method,
            },
        },
    )


# ── Uvicorn Dev Entry Point ────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    setup_logging()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_config=None,  # Disable uvicorn's default logger; Loguru handles all logs
    )
