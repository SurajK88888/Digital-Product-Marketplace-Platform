"""
tests/test_health.py — Unit Tests for Health Check Probes
===========================================================
Verifies that the API server liveness and readiness endpoints respond correctly.
"""

# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_liveness_probe() -> None:
    """Verify that the /api/v1/health/live endpoint returns 200 OK and status alive."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"
    assert "version" in data
    assert "environment" in data
