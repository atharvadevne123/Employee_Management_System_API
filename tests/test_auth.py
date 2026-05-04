"""Tests for JWT authentication endpoints."""
from __future__ import annotations

import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestJWTAuth:
    """Test suite for JWT token obtain and refresh endpoints."""

    def test_obtain_token_with_valid_credentials(self, api_client):
        """Valid credentials return access and refresh tokens."""
        User.objects.create_user(username="authuser", password="strongpass99")
        response = api_client.post(
            "/api/token/",
            {"username": "authuser", "password": "strongpass99"},
        )
        assert response.status_code == 200
        assert "access" in response.data
        assert "refresh" in response.data

    def test_obtain_token_with_invalid_credentials(self, api_client):
        """Invalid credentials return 401."""
        response = api_client.post(
            "/api/token/",
            {"username": "nobody", "password": "wrongpass"},
        )
        assert response.status_code == 401

    def test_refresh_token(self, api_client):
        """Valid refresh token returns new access token."""
        User.objects.create_user(username="refreshuser", password="refreshpass99")
        obtain = api_client.post(
            "/api/token/",
            {"username": "refreshuser", "password": "refreshpass99"},
        )
        refresh_token = obtain.data["refresh"]
        response = api_client.post("/api/token/refresh/", {"refresh": refresh_token})
        assert response.status_code == 200
        assert "access" in response.data

    def test_refresh_with_invalid_token(self, api_client):
        """Invalid refresh token returns 401."""
        response = api_client.post("/api/token/refresh/", {"refresh": "not.a.valid.token"})
        assert response.status_code == 401

    def test_protected_endpoint_without_token(self, api_client):
        """Accessing protected endpoint without token returns 401."""
        response = api_client.get("/api/employees/employees/")
        assert response.status_code == 401

    def test_protected_endpoint_with_valid_token(self, api_client):
        """Accessing protected endpoint with valid token returns 200."""
        user = User.objects.create_user(username="tokenuser", password="tokenpass99")
        obtain = api_client.post(
            "/api/token/",
            {"username": "tokenuser", "password": "tokenpass99"},
        )
        access = obtain.data["access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = api_client.get("/api/employees/employees/")
        assert response.status_code == 200

    def test_protected_endpoint_with_expired_token(self, api_client):
        """Malformed token returns 401."""
        api_client.credentials(HTTP_AUTHORIZATION="Bearer eyInvalid.Token.Here")
        response = api_client.get("/api/employees/employees/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestHealthEndpoints:
    """Test suite for health and version endpoints."""

    def test_health_check_returns_200(self, api_client):
        """Health endpoint returns 200 without authentication."""
        response = api_client.get("/api/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_version_endpoint_returns_version(self, api_client):
        """Version endpoint returns version string."""
        response = api_client.get("/api/version/")
        assert response.status_code == 200
        assert "version" in response.json()
