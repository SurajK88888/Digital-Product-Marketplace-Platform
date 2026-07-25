"""
app/core/exceptions.py — Custom Domain Exception Hierarchy
============================================================
Defines a structured exception hierarchy for the entire application.
FastAPI exception handlers in main.py map these to standardized
RFC 7807 JSON error responses.

Reusable pattern: Add new exception classes here as domain grows.
Never raise raw HTTPException inside service/domain layers —
always use these typed exceptions to preserve clean architecture.
"""

from http import HTTPStatus
from typing import Any


class MarketplaceBaseException(Exception):
    """
    Base exception for all application-specific errors.
    All custom exceptions must inherit from this class.
    """

    status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR.value
    code: str = "INTERNAL_ERROR"
    message: str = "An unexpected error occurred."

    def __init__(
        self,
        *,
        message: str | None = None,
        code: str | None = None,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        self.message = message or self.__class__.message
        self.code = code or self.__class__.code
        self.details = details or []
        super().__init__(self.message)


# ── 400 Bad Request ───────────────────────────────────────────
class BadRequestException(MarketplaceBaseException):
    status_code = HTTPStatus.BAD_REQUEST.value
    code = "BAD_REQUEST"
    message = "The request is malformed or invalid."


# ── 401 Unauthorized ──────────────────────────────────────────
class UnauthorizedException(MarketplaceBaseException):
    status_code = HTTPStatus.UNAUTHORIZED.value
    code = "UNAUTHORIZED"
    message = "Authentication is required to access this resource."


# ── 403 Forbidden ─────────────────────────────────────────────
class ForbiddenException(MarketplaceBaseException):
    status_code = HTTPStatus.FORBIDDEN.value
    code = "FORBIDDEN"
    message = "You do not have permission to perform this action."


# ── 404 Not Found ─────────────────────────────────────────────
class NotFoundException(MarketplaceBaseException):
    status_code = HTTPStatus.NOT_FOUND.value
    code = "NOT_FOUND"
    message = "The requested resource was not found."


# ── 409 Conflict ──────────────────────────────────────────────
class ConflictException(MarketplaceBaseException):
    status_code = HTTPStatus.CONFLICT.value
    code = "CONFLICT"
    message = "A conflict occurred with the current state of the resource."


# ── 422 Unprocessable Entity ──────────────────────────────────
class ValidationException(MarketplaceBaseException):
    status_code = HTTPStatus.UNPROCESSABLE_ENTITY.value
    code = "VALIDATION_FAILED"
    message = "The request payload failed schema validation."


# ── 429 Too Many Requests ────────────────────────────────────
class RateLimitException(MarketplaceBaseException):
    status_code = HTTPStatus.TOO_MANY_REQUESTS.value
    code = "RATE_LIMIT_EXCEEDED"
    message = "Too many requests. Please slow down."


# ── Domain-Specific Exceptions ────────────────────────────────
class LicenseExpiredException(ForbiddenException):
    code = "LICENSE_EXPIRED"
    message = "Your license for this product has expired."


class LicenseRevokedException(ForbiddenException):
    code = "LICENSE_REVOKED"
    message = "Your license for this product has been revoked."


class DownloadLimitExceededException(ForbiddenException):
    code = "DOWNLOAD_LIMIT_EXCEEDED"
    message = "You have reached the maximum number of downloads for this license."


class PaymentRequiredException(MarketplaceBaseException):
    status_code = HTTPStatus.PAYMENT_REQUIRED.value
    code = "PAYMENT_REQUIRED"
    message = "Payment is required to access this resource."


class ConcurrencyConflictException(ConflictException):
    code = "CONCURRENCY_CONFLICT"
    message = "The resource was modified by another request. Please retry."
