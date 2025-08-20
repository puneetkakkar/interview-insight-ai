import pytest
from fastapi.testclient import TestClient
from src.app.main import app


def test_health_success_envelope():
    with TestClient(app) as client:
        resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert isinstance(body["data"], dict)
    assert body["data"]["status"] == "healthy"


def test_root_success_envelope():
    with TestClient(app) as client:
        resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert isinstance(body["data"], dict)
    assert "version" in body["data"]


def test_info_success_envelope():
    with TestClient(app) as client:
        resp = client.get("/info")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert isinstance(body["data"], dict)
    assert body["data"]["status"] == "running"


def test_validation_error_envelope():
    # limit must be >= 1; sending 0 triggers validation error
    with TestClient(app) as client:
        resp = client.get("/api/v1/items", params={"limit": 0})
    assert resp.status_code == 422
    body = resp.json()
    assert body["success"] is False
    assert body["data"] is None
    assert "error" in body
    assert body["error"]["code"] == 422
    assert body["error"]["message"] == "Validation Error"
    assert isinstance(body["error"]["details"], list)
    assert any(
        d.get("type") == "greater_than_equal" or d.get("msg", "").lower().find("greater than or equal") != -1
        for d in body["error"]["details"]
    )


