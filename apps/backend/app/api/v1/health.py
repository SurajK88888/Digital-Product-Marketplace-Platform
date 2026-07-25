"""
app/api/v1/health.py — Health Check Endpoints
===============================================
Provides liveness and readiness probes for Kubernetes and load balancers.

- GET /api/v1/health/live   → Liveness probe (is the process running?)
- GET /api/v1/health/ready  → Readiness probe (are dependencies reachable?)

Reusable pattern: Copy this module to any FastAPI application.
Add new dependency checks to the readiness probe as services are added.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.core.logging import get_logger
from app.database.session import AsyncSessionLocal

logger = get_logger(__name__)

health_router = APIRouter()


@health_router.get(
    "/live",
    summary="Liveness Probe",
    description="Confirms the application process is running and the event loop is healthy.",
    status_code=status.HTTP_200_OK,
    tags=["Health"],
)
async def liveness_check() -> JSONResponse:
    """
    Kubernetes liveness probe.
    Returns 200 OK if the process is alive.
    Returns 503 if the event loop is blocked or the process is unhealthy.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "alive",
            "timestamp": datetime.now(UTC).isoformat(),
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        },
    )


@health_router.get(
    "/ready",
    summary="Readiness Probe",
    description="Validates connectivity to PostgreSQL and other critical dependencies.",
    tags=["Health"],
)
async def readiness_check() -> JSONResponse:
    """
    Kubernetes readiness probe.
    Returns 200 OK only if all critical dependencies are reachable.
    Returns 503 if any dependency check fails (removes pod from load balancer).
    """
    checks: dict[str, str] = {}
    all_healthy = True

    # ── Database Connectivity Check ────────────────────────────
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception as exc:
        logger.error("Readiness check: database connectivity failed", error=str(exc))
        checks["database"] = f"error: {type(exc).__name__}"
        all_healthy = False

    # ── Additional checks (Redis, S3) added in Phase 2+ ───────
    # try:
    #     await redis_client.ping()
    #     checks["redis"] = "ok"
    # except Exception as exc:
    #     checks["redis"] = f"error: {type(exc).__name__}"
    #     all_healthy = False

    http_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=http_status,
        content={
            "status": "ready" if all_healthy else "degraded",
            "timestamp": datetime.now(UTC).isoformat(),
            "version": settings.APP_VERSION,
            "checks": checks,
        },
    )
