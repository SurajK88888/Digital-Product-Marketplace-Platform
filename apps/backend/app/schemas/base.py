"""
app/schemas/base.py — Base Pydantic Schemas & Response Models
==============================================================
Defines the universal API response envelope and error schemas.
All route responses must wrap their data in these models to maintain
frontend compatibility and RFC 7807 compliance.

Reusable pattern: Copy these base schemas to any FastAPI project.
"""

from datetime import UTC, datetime
from typing import Any, Generic, TypeVar
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

# ── Generic Type Variable ─────────────────────────────────────
DataT = TypeVar("DataT")


class BaseSchema(BaseModel):
    """
    Base Pydantic schema with shared configuration.
    All application schemas inherit from this class.
    """

    model_config = ConfigDict(
        # Allow ORM model instances to be passed directly
        from_attributes=True,
        # Use enum values, not enum objects, in JSON output
        use_enum_values=True,
        # Strip leading/trailing whitespace from string fields
        str_strip_whitespace=True,
        # Populate fields from their aliases too
        populate_by_name=True,
    )


# ── Response Meta ─────────────────────────────────────────────
class ResponseMeta(BaseModel):
    """Metadata block included in every API response."""

    timestamp: str = Field(
        default_factory=lambda: datetime.now(UTC).isoformat() + "Z"
    )
    version: str = "v1"
    request_id: str = Field(default_factory=lambda: str(uuid4()))


# ── Success Response Envelope ─────────────────────────────────
class ApiResponse(BaseModel, Generic[DataT]):
    """
    Standard success response wrapper.

    Usage:
        @router.get("/", response_model=ApiResponse[ProductOut])
        async def list_products():
            return ApiResponse(data=products)
    """

    success: bool = True
    data: DataT
    meta: ResponseMeta = Field(default_factory=ResponseMeta)


# ── Error Detail ──────────────────────────────────────────────
class ErrorDetail(BaseModel):
    """Individual field validation error detail."""

    field: str
    reason: str


# ── Error Response Envelope ───────────────────────────────────
class ErrorBody(BaseModel):
    """The `error` object inside an error response."""

    code: str
    message: str
    details: list[ErrorDetail] = Field(default_factory=list)
    trace_id: str | None = None


class ErrorResponse(BaseModel):
    """
    Standard error response wrapper (RFC 7807 inspired).
    Returned by all exception handlers in main.py.
    """

    success: bool = False
    error: ErrorBody
    meta: dict[str, Any]


# ── Pagination Meta ───────────────────────────────────────────
class PaginationMeta(BaseModel):
    """Cursor-based pagination metadata."""

    limit: int
    has_next_page: bool
    next_cursor: str | None = None
    total_count: int | None = None


class PaginatedResponse(BaseModel, Generic[DataT]):
    """
    Paginated list response wrapper with cursor-based pagination.

    Usage:
        return PaginatedResponse(data=items, pagination=pagination_meta)
    """

    success: bool = True
    data: list[DataT]
    meta: ResponseMeta = Field(default_factory=ResponseMeta)
    pagination: PaginationMeta
