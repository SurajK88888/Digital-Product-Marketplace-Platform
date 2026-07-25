"""
app/api/v1/router.py — API v1 Root Router
==========================================
Aggregates all v1 domain routers into a single router
that is mounted by main.py under /api/v1.

Reusable pattern: Add new domain routers here as the project grows.
Example: from app.modules.auth.controllers import auth_router
"""

from fastapi import APIRouter

from app.api.v1.health import health_router

# ── v1 Root Router ────────────────────────────────────────────
api_v1_router = APIRouter()

# ── Domain Routers (registered here as modules are built in Phase 2+) ──
api_v1_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

# Phase 2+ routers will be added below:
# api_v1_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
# api_v1_router.include_router(users_router, prefix="/users", tags=["Users"])
# api_v1_router.include_router(products_router, prefix="/products", tags=["Catalog"])
# api_v1_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
# api_v1_router.include_router(downloads_router, prefix="/downloads", tags=["Downloads"])
