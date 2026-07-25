"""
app/middleware/correlation.py — Correlation ID Middleware
=========================================================
Injects a unique X-Request-Id into every request for distributed tracing.
The ID is propagated to logs, database queries, and async queue jobs,
enabling full-stack trace reconstruction in Datadog/Grafana.

Reusable pattern: Add this middleware to any FastAPI application.
"""

import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

CORRELATION_ID_HEADER = "X-Request-Id"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """
    ASGI middleware that ensures every request has a correlation ID.

    - If the client sends X-Request-Id, it is reused (trusted upstream).
    - Otherwise a new UUID v4 is generated server-side.
    - The ID is echoed back in the response header.
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # Reuse client-provided ID or generate a new one
        correlation_id = request.headers.get(CORRELATION_ID_HEADER, str(uuid.uuid4()))

        # Attach to request state for access in route handlers and loggers
        request.state.correlation_id = correlation_id

        response = await call_next(request)

        # Echo back in response headers for client-side correlation
        response.headers[CORRELATION_ID_HEADER] = correlation_id

        return response
