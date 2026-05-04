"""Tests for DRF serializers."""
from __future__ import annotations

import pytest


@pytest.mark.django_db
class TestEmployeeSerializer:
    """Tests for EmployeeSerializer validation logic."""

    def test_email_is_lowercased(self, department, db):
        """Email input is normalized to lowercase."""
        from employees.serializers import EmployeeSerializer

        data = {
            "first_name": "Test",
            "last_name": "User",
            "email": "TEST.USER@EXAMPLE.COM",
            "department": department.id,
            "job_title": "Developer",
            "salary": "60000.00",
        }
        serializer = EmployeeSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        assert serializer.validated_data["email"] == "test.user@example.com"

    def test_negative_salary_invalid(self, department, db):
        """Negative salary makes serializer invalid."""
        from employees.serializers import EmployeeSerializer

        data = {
            "first_name": "Bad",
            "last_name": "Salary",
            "email": "bad.salary@example.com",
            "department": department.id,
            "job_title": "Engineer",
            "salary": "-500",
        }
        serializer = EmployeeSerializer(data=data)
        assert not serializer.is_valid()
        assert "salary" in serializer.errors

    def test_employee_count_in_department_serializer(self, department, employee, db):
        """DepartmentSerializer employee_count reflects active employees."""
        from employees.serializers import DepartmentSerializer

        serializer = DepartmentSerializer(instance=department)
        assert serializer.data["employee_count"] == 1


@pytest.mark.django_db
class TestAttendanceSerializer:
    """Tests for AttendanceRecordSerializer validation."""

    def test_check_out_before_check_in_invalid(self, employee, db):
        """Serializer rejects check_out before check_in."""
        from attendance.serializers import AttendanceRecordSerializer

        data = {
            "employee": employee.id,
            "date": "2025-06-01",
            "check_in": "17:00:00",
            "check_out": "09:00:00",
            "status": "present",
        }
        serializer = AttendanceRecordSerializer(data=data)
        assert not serializer.is_valid()
        assert "check_out" in serializer.errors

    def test_valid_attendance_record(self, employee, db):
        """Serializer accepts valid attendance data."""
        from attendance.serializers import AttendanceRecordSerializer

        data = {
            "employee": employee.id,
            "date": "2025-06-15",
            "check_in": "09:00:00",
            "check_out": "17:00:00",
            "status": "present",
        }
        serializer = AttendanceRecordSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
