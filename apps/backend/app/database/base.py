"""
app/database/base.py — SQLAlchemy Declarative Base & Audit Mixin
=================================================================
Defines the shared base class and reusable audit mixin for all ORM models.
Every database table in the system inherits from `Base` and `AuditMixin`.

Reusable pattern: Copy `AuditMixin` to any SQLAlchemy project.
It provides automatic created_at, updated_at, soft delete, and versioning
columns on every table.
"""

from datetime import UTC, datetime
import uuid

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    SQLAlchemy Declarative Base.
    All ORM models must inherit from this class.
    """

    pass


class AuditMixin:
    """
    Audit Mixin — Reusable audit trail columns.
    =============================================
    Provides the following columns on every table:
    - id: UUID primary key (auto-generated)
    - created_at: Timestamp of record creation
    - updated_at: Timestamp of last update (auto-updates via onupdate)
    - deleted_at: Soft delete timestamp (NULL = active)
    - version_num: Optimistic concurrency control counter

    Reusable pattern: Inherit this mixin on every SQLAlchemy model.

    Usage:
        class User(Base, AuditMixin):
            __tablename__ = "users"
            email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    """

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=False),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        nullable=False,
        comment="UUID v4 primary key — never expose sequential IDs",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp (UTC)",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
        comment="Last modification timestamp (UTC, auto-updated)",
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Soft delete timestamp. NULL = active record.",
    )

    version_num: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        comment="Optimistic concurrency control version counter",
    )

    @property
    def is_deleted(self) -> bool:
        """True if this record has been soft-deleted."""
        return self.deleted_at is not None

    def soft_delete(self) -> None:
        """Mark record as deleted without removing the database row."""
        self.deleted_at = datetime.now(UTC)
