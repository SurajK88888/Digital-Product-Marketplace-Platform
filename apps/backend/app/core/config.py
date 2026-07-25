"""
app/core/config.py — Typed Application Configuration
======================================================
All configuration is loaded from environment variables via Pydantic BaseSettings.
This guarantees:
1. Type safety — wrong types fail at startup, not runtime.
2. Zero hardcoding — no secrets in source code.
3. Environment isolation — dev/staging/prod via .env files.

Reusable pattern: Copy this module to any FastAPI project.
Add new settings fields here; document them in .env.example.
"""

from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    All fields are required unless a default is provided.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore unknown env vars (safe for CI/CD environments)
    )

    # ── Application ───────────────────────────────────────────
    APP_NAME: str = "Digital Product Marketplace API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False

    # ── Database (PostgreSQL) ─────────────────────────────────
    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int = 10          # Connections per worker process
    DB_MAX_OVERFLOW: int = 20       # Extra connections above pool size
    DB_POOL_TIMEOUT: int = 30       # Seconds to wait for a free connection
    DB_ECHO_SQL: bool = False       # Log raw SQL queries (dev only)

    # ── Redis ─────────────────────────────────────────────────
    REDIS_URL: RedisDsn = "redis://localhost:6379/0"  # type: ignore[assignment]

    # ── Security & JWT ────────────────────────────────────────
    SECRET_KEY: str                 # Must be ≥64 chars in production
    ALGORITHM: str = "HS256"        # JWT signing algorithm
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── CORS ──────────────────────────────────────────────────
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Allow comma-separated string or JSON array in env var."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # ── AWS / Storage ─────────────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: str = "marketplace-product-vault"
    DOWNLOAD_URL_EXPIRY_SECONDS: int = 300  # 5 minutes for presigned URLs

    # ── Email ─────────────────────────────────────────────────
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@marketplace.com"

    # ── OAuth ─────────────────────────────────────────────────
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""

    # ── Stripe ────────────────────────────────────────────────
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""

    # ── Observability ─────────────────────────────────────────
    SENTRY_DSN: str = ""
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Cached settings factory.
    The @lru_cache ensures settings are loaded once and reused.
    Reusable pattern: Use Depends(get_settings) in FastAPI dependency injection.
    """
    return Settings()  # type: ignore[call-arg]


# ── Singleton export ───────────────────────────────────────────
settings: Settings = get_settings()
