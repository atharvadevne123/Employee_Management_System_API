"""Tests for custom pagination behaviour."""
from __future__ import annotations

import pytest


@pytest.mark.django_db
class TestStandardPagination:
    """Tests for paginated list responses."""

    def test_list_response_has_pagination_keys(self, auth_client, employee):
        """List response includes count, next, previous, and results."""
        response = auth_client.get("/api/employees/employees/")
        assert response.status_code == 200
        assert "count" in response.data
        assert "results" in response.data
        assert "next" in response.data
        assert "previous" in response.data

    def test_page_size_query_param(self, auth_client, employee, second_employee):
        """page_size param limits results per page."""
        response = auth_client.get("/api/employees/employees/?page_size=1")
        assert response.status_code == 200
        assert len(response.data["results"]) == 1

    def test_department_list_is_paginated(self, auth_client, department):
        """Department list also returns paginated response."""
        response = auth_client.get("/api/employees/departments/")
        assert response.status_code == 200
        assert "count" in response.data
        assert "results" in response.data

    def test_attendance_list_is_paginated(self, auth_client, attendance_record):
        """Attendance list returns paginated response."""
        response = auth_client.get("/api/attendance/records/")
        assert response.status_code == 200
        assert "count" in response.data
