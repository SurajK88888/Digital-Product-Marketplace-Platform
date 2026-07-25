"""
app/core/dependencies.py — FastAPI Dependency Injection Container
==================================================================
Provides reusable FastAPI dependencies for authentication, database sessions,
and settings. Injected via `Depends()` in route handlers.

Reusable pattern: Add new dependencies here.
Never instantiate DB sessions or auth logic directly in route handlers.
"""

from typing import Annotated

from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token
from app.database.session import get_db_session

# ── Dependency Type Aliases ────────────────────────────────────
# Use these type aliases in route signatures for concise, readable code.
# Example: async def my_route(db: DbSession, user: CurrentUser): ...

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
AppSettings = Annotated[Settings, Depends(get_settings)]

# ── HTTP Bearer Token Extractor ───────────────────────────────
bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Security(bearer_scheme)
    ] = None,
) -> str:
    """
    Extract and validate the Bearer JWT from the Authorization header.
    Returns the authenticated user's UUID string.
    Raises UnauthorizedException if token is missing or invalid.

    Reusable pattern: Use `CurrentUserId` in any protected route.
    """
    if not credentials or not credentials.credentials:
        raise UnauthorizedException(
            message="Authorization header with Bearer token is required.",
            code="TOKEN_MISSING",
        )

    payload = decode_access_token(credentials.credentials)
    user_id: str | None = payload.get("sub")

    if not user_id:
        raise UnauthorizedException(
            message="Token subject (user ID) is missing.",
            code="TOKEN_INVALID_SUBJECT",
        )

    return user_id


CurrentUserId = Annotated[str, Depends(get_current_user_id)]
