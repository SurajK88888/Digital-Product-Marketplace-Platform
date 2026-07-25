"""
app/core/logging.py — Structured Logging Framework
====================================================
Configures Loguru as the sole logging sink for the entire application.
Outputs structured JSON logs in production and human-readable colored
logs in development.

Reusable pattern: Call `setup_logging()` once at application startup.
Use `get_logger(__name__)` in every module for contextualized logging.
"""

import logging
import sys
from typing import Any

from loguru import logger

from app.core.config import settings


class InterceptHandler(logging.Handler):
    """
    Intercepts standard library `logging` calls and routes them to Loguru.
    Ensures uvicorn, SQLAlchemy, and other library logs use our format.
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Find the correct Loguru level
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find the caller to report the correct source module
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            if frame.f_back:
                frame = frame.f_back
                depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging() -> None:
    """
    Initialize the logging configuration for the entire application.
    Call once at startup in main.py.
    """
    # Remove Loguru's default handler
    logger.remove()

    if settings.ENVIRONMENT == "production":
        # ── Production: Structured JSON output ────────────────
        logger.add(
            sys.stdout,
            level=settings.LOG_LEVEL,
            format="{message}",
            serialize=True,  # Outputs valid JSON lines
            backtrace=False,
            diagnose=False,  # Never expose locals in production
        )
    else:
        # ── Development: Colored, readable output ─────────────
        logger.add(
            sys.stdout,
            level="DEBUG",
            colorize=True,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
            backtrace=True,
            diagnose=True,
        )

    # ── Intercept standard library loggers ────────────────────
    # Captures uvicorn, SQLAlchemy, httpx, etc.
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    for log_name in ["uvicorn", "uvicorn.error", "fastapi", "sqlalchemy.engine"]:
        log = logging.getLogger(log_name)
        log.handlers = [InterceptHandler()]
        log.propagate = False


def get_logger(name: str) -> Any:
    """
    Get a contextualized logger bound to the calling module name.

    Usage:
        logger = get_logger(__name__)
        logger.info("Processing request", user_id=user.id, order_id=order.id)
    """
    return logger.bind(module=name)
