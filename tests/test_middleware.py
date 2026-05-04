"""Tests for custom middleware."""
from __future__ import annotations

import pytest


@pytest.mark.django_db
class TestRequestIDMiddleware:
    """Tests for RequestIDMiddleware."""

    def test_response_has_x_request_id_header(self, api_client):
        """Every response includes an X-Request-ID header."""
        response = api_client.get("/api/health/")
        assert "X-Request-ID" in response

    def test_custom_request_id_is_echoed(self, api_client):
        """If X-Request-ID is sent in request, it is echoed in response."""
        custom_id = "my-custom-id-12345"
        response = api_client.get(
            "/api/health/",
            HTTP_X_REQUEST_ID=custom_id,
        )
        assert response.get("X-Request-ID") == custom_id

    def test_auto_generated_id_is_uuid_format(self, api_client):
        """Auto-generated X-Request-ID is a valid UUID."""
        import uuid

        response = api_client.get("/api/health/")
        request_id = response.get("X-Request-ID")
        parsed = uuid.UUID(request_id, version=4)
        assert str(parsed) == request_id


@pytest.mark.django_db
class TestHealthEndpoint:
    """Tests for the health and version utility endpoints."""

    def test_health_returns_ok(self, api_client):
        """Health endpoint returns status=ok."""
        response = api_client.get("/api/health/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data

    def test_version_returns_version_string(self, api_client):
        """Version endpoint returns a version key."""
        response = api_client.get("/api/version/")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"
