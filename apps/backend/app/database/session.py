"""
app/database/session.py — Async Database Session Factory
=========================================================
Configures SQLAlchemy async engine and session factory.
All database I/O uses async/await for non-blocking operation.

Reusable pattern: Import `get_db_session` as a FastAPI dependency.
Never create sessions manually in route handlers.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# ── Async Engine ──────────────────────────────────────────────
# Uses asyncpg driver for maximum PostgreSQL throughput
engine: AsyncEngine = create_async_engine(
    str(settings.DATABASE_URL),
    # ── Connection Pool ────────────────────────────────────────
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_pre_ping=True,  # Validate connections before use (handles stale connections)
    pool_recycle=3600,  # Recycle connections after 1 hour
    # ── Debugging ─────────────────────────────────────────────
    echo=settings.DB_ECHO_SQL,
    echo_pool=False,
)

# ── Async Session Factory ─────────────────────────────────────
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Prevent lazy-load errors after commit
    autocommit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an async database session.
    Automatically commits on success and rolls back on exception.

    Usage in routes:
        async def my_route(db: Annotated[AsyncSession, Depends(get_db_session)]):
            ...
    Or use the alias from dependencies.py:
        async def my_route(db: DbSession):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
