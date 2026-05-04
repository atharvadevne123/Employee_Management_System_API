"""Pytest fixtures for Employee Management System API test suite."""
from __future__ import annotations

import os

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "employee_project.settings")
os.environ["USE_SQLITE"] = "True"
django.setup()

from django.contrib.auth.models import User  # noqa: E402

from attendance.models import AttendanceRecord  # noqa: E402
from employees.models import Department, Employee, PerformanceReview  # noqa: E402


@pytest.fixture(scope="session")
def django_db_setup():
    """Use the default test database."""


@pytest.fixture
def department(db) -> Department:
    """Return a saved Department fixture."""
    return Department.objects.create(
        name="Engineering",
        description="Software development team",
    )


@pytest.fixture
def employee(db, department: Department) -> Employee:
    """Return a saved Employee fixture."""
    return Employee.objects.create(
        first_name="Jane",
        last_name="Doe",
        email="jane.doe@example.com",
        phone="555-1234",
        department=department,
        job_title="Software Engineer",
        salary=90000,
        status="active",
    )


@pytest.fixture
def second_employee(db, department: Department) -> Employee:
    """Return a second saved Employee fixture."""
    return Employee.objects.create(
        first_name="John",
        last_name="Smith",
        email="john.smith@example.com",
        department=department,
        job_title="QA Engineer",
        salary=75000,
        status="active",
    )


@pytest.fixture
def performance_review(db, employee: Employee) -> PerformanceReview:
    """Return a saved PerformanceReview fixture."""
    return PerformanceReview.objects.create(
        employee=employee,
        reviewer="Alice Manager",
        rating="meets_expectations",
        comments="Good work overall.",
        goals="Improve test coverage.",
    )


@pytest.fixture
def attendance_record(db, employee: Employee) -> AttendanceRecord:
    """Return a saved AttendanceRecord fixture."""
    from datetime import time

    return AttendanceRecord.objects.create(
        employee=employee,
        status="present",
        check_in=time(9, 0),
        check_out=time(17, 30),
    )


@pytest.fixture
def api_client():
    """Return a DRF APIClient instance."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def auth_client(db, api_client):
    """Return an authenticated DRF APIClient."""
    user = User.objects.create_user(username="testuser", password="testpass123")
    api_client.force_authenticate(user=user)
    return api_client
