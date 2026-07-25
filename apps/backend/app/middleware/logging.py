"""
app/middleware/logging.py — Request/Response Logging Middleware
===============================================================
Logs every HTTP request and response with structured metadata:
method, path, status code, duration, and correlation ID.
Sensitive routes (auth endpoints) redact request bodies from logs.

Reusable pattern: Add this to any FastAPI app for automatic access logging.
"""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from app.core.logging import get_logger

logger = get_logger(__name__)

# ── Routes whose request bodies are redacted from logs ────────
SENSITIVE_PATHS = {"/api/v1/auth/login", "/api/v1/auth/register", "/api/v1/auth/refresh"}


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    ASGI middleware that logs structured access logs for every HTTP request.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        start_time = time.perf_counter()

        # Log incoming request
        logger.info(
            "→ Incoming request",
            method=request.method,
            path=request.url.path,
            query=str(request.url.query) or None,
            correlation_id=correlation_id,
            client_ip=request.client.host if request.client else "unknown",
            user_agent=request.headers.get("User-Agent", "unknown"),
        )

        try:
            response = await call_next(request)
        except Exception as exc:
            duration_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                "✗ Request failed with exception",
                method=request.method,
                path=request.url.path,
                duration_ms=round(duration_ms, 2),
                correlation_id=correlation_id,
                error=str(exc),
            )
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000
        status_code = response.status_code

        log_fn = logger.warning if status_code >= 400 else logger.info
        log_fn(
            "← Request completed",
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            duration_ms=round(duration_ms, 2),
            correlation_id=correlation_id,
        )

        return response
