"""Tests for custom permission classes."""
from __future__ import annotations

import pytest


@pytest.mark.django_db
class TestIsAdminOrReadOnly:
    """Tests for IsAdminOrReadOnly permission class."""

    def test_unauthenticated_get_returns_401(self, api_client, department):
        """Unauthenticated GET returns 401."""
        response = api_client.get("/api/employees/departments/")
        assert response.status_code == 401

    def test_authenticated_get_succeeds(self, auth_client, department):
        """Authenticated GET returns 200."""
        response = auth_client.get("/api/employees/departments/")
        assert response.status_code == 200

    def test_authenticated_post_succeeds_for_regular_user(self, auth_client):
        """Regular authenticated user can POST (IsAuthenticated default)."""
        response = auth_client.post(
            "/api/employees/departments/",
            {"name": "PermTest", "description": "Testing"},
        )
        assert response.status_code == 201


@pytest.mark.django_db
class TestByDepartmentAction:
    """Tests for the by-department custom action."""

    def test_by_department_returns_list(self, auth_client, department, employee):
        """by-department returns list with id, name, count."""
        response = auth_client.get("/api/employees/employees/by-department/")
        assert response.status_code == 200
        assert isinstance(response.data, list)
        entry = next((d for d in response.data if d["name"] == department.name), None)
        assert entry is not None
        assert entry["count"] >= 1
