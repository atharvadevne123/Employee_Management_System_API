"""Tests for custom FilterSet classes."""
from __future__ import annotations

import pytest


@pytest.mark.django_db
class TestEmployeeFilter:
    """Tests for EmployeeFilter salary/name filtering."""

    def test_filter_by_salary_min(self, auth_client, employee):
        """salary_min excludes employees below the threshold."""
        below_salary = employee.salary - 1
        response = auth_client.get(f"/api/employees/employees/?salary_min={below_salary}")
        assert response.status_code == 200
        assert response.data["count"] >= 1

    def test_filter_by_salary_max_zero_returns_empty(self, auth_client, employee):
        """salary_max=0 excludes all employees with salary > 0."""
        response = auth_client.get("/api/employees/employees/?salary_max=0")
        assert response.status_code == 200
        assert response.data["count"] == 0

    def test_filter_by_name(self, auth_client, employee):
        """name filter matches first or last name case-insensitively."""
        response = auth_client.get(
            f"/api/employees/employees/?name={employee.first_name.lower()}"
        )
        assert response.status_code == 200
        assert response.data["count"] >= 1

    def test_filter_hire_after(self, auth_client, employee):
        """hire_after filter excludes employees hired before the date."""
        response = auth_client.get("/api/employees/employees/?hire_after=2000-01-01")
        assert response.status_code == 200
        assert response.data["count"] >= 1


@pytest.mark.django_db
class TestAttendanceFilter:
    """Tests for AttendanceFilter date range filtering."""

    def test_filter_by_status_present(self, auth_client, attendance_record):
        """status=present returns only present records."""
        response = auth_client.get("/api/attendance/records/?status=present")
        assert response.status_code == 200
        for record in response.data["results"]:
            assert record["status"] == "present"

    def test_filter_by_employee_name(self, auth_client, attendance_record, employee):
        """employee_name filter matches by employee first name."""
        response = auth_client.get(
            f"/api/attendance/records/?employee_name={employee.first_name}"
        )
        assert response.status_code == 200
        assert response.data["count"] >= 1

    def test_filter_date_after_future_returns_empty(self, auth_client, attendance_record):
        """date_after far in the future returns zero results."""
        response = auth_client.get("/api/attendance/records/?date_after=2099-01-01")
        assert response.status_code == 200
        assert response.data["count"] == 0
