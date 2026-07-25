"""
alembic/env.py — Alembic Migration Environment
================================================
Configures Alembic to use async SQLAlchemy engine and auto-imports
all ORM models for autogenerate support.

Reusable pattern: Import all models at the bottom of this file
so Alembic can detect schema changes automatically.
"""

import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.core.config import settings
from app.database.base import Base

# ── Import all models here for autogenerate detection ──────────
# As new modules are built (Phase 2+), import their models below.
# from app.modules.users.models import User
# from app.modules.products.models import Product, ProductVariant
# from app.modules.orders.models import Order, OrderItem

# ── Alembic Config ────────────────────────────────────────────
config = context.config

# Override the sqlalchemy.url with the value from application settings
# This guarantees .env is the single source of truth — never alembic.ini
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))

# Set up logging from alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (generate SQL script without DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # Detect column type changes
        compare_server_default=True,  # Detect server default changes
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations using async engine (required for asyncpg driver)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Use NullPool for migration runs (no connection reuse)
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (directly against the database)."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
