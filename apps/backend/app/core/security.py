"""
app/core/security.py — Authentication & Cryptographic Utilities
================================================================
Provides JWT creation/validation, password hashing, and secure token generation.
All security operations are centralized here — never scattered across modules.

Reusable pattern: Import `create_access_token`, `verify_password`,
and `hash_password` in any FastAPI auth module.
"""

from datetime import UTC, datetime, timedelta
import secrets
from typing import Any, cast
import uuid

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import UnauthorizedException

# ── Password Hashing Context ──────────────────────────────────
# bcrypt with automatic cost factor tuning
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ── JWT Token Claims Model ────────────────────────────────────
TOKEN_TYPE_ACCESS = "access"
TOKEN_TYPE_REFRESH = "refresh"


def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password using bcrypt.
    The hash includes the salt — no separate salt storage needed.
    """
    return cast(str, pwd_context.hash(plain_password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a bcrypt hash.
    Uses constant-time comparison to prevent timing attacks.
    """
    return cast(bool, pwd_context.verify(plain_password, hashed_password))


def create_access_token(
    subject: str,
    *,
    additional_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: The user UUID (stored as JWT `sub` claim).
        additional_claims: Extra payload (e.g., role, email, sessionId).
        expires_delta: Custom expiry override (defaults to settings).

    Returns:
        Signed JWT string.
    """
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": datetime.now(UTC),
        "exp": expire,
        "type": TOKEN_TYPE_ACCESS,
        "jti": str(uuid.uuid4()),  # Unique token ID for revocation
    }

    if additional_claims:
        payload.update(additional_claims)

    return cast(str, jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM))


def create_refresh_token() -> str:
    """
    Generate a cryptographically secure opaque refresh token.
    This is NOT a JWT — it is a random 64-byte hex string stored in Redis.
    Stored in an HttpOnly cookie on the client side.
    """
    return secrets.token_hex(64)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.
    Raises UnauthorizedException if expired, malformed, or wrong type.

    Returns:
        Decoded JWT payload dict.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
    except JWTError as exc:
        raise UnauthorizedException(
            message="Invalid or expired access token.",
            code="TOKEN_INVALID",
        ) from exc

    if payload.get("type") != TOKEN_TYPE_ACCESS:
        raise UnauthorizedException(
            message="Invalid token type.",
            code="TOKEN_TYPE_MISMATCH",
        )

    return cast(dict[str, Any], payload)


def generate_verification_token() -> str:
    """Generate a secure URL-safe token for email verification or password reset."""
    return secrets.token_urlsafe(32)
