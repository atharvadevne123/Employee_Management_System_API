"""Tests for the attendance API endpoints."""
from __future__ import annotations

from datetime import date, time

import pytest


@pytest.mark.django_db
class TestAttendanceAPI:
    """Test suite for AttendanceRecord CRUD endpoints."""

    def test_list_attendance_requires_auth(self, api_client):
        """Unauthenticated request returns 401."""
        response = api_client.get("/api/attendance/records/")
        assert response.status_code == 401

    def test_list_attendance(self, auth_client, attendance_record):
        """Authenticated list returns paginated attendance records."""
        response = auth_client.get("/api/attendance/records/")
        assert response.status_code == 200
        assert response.data["count"] >= 1

    def test_create_attendance_record(self, auth_client, employee):
        """POST creates a new attendance record."""
        payload = {
            "employee": employee.id,
            "date": str(date(2025, 1, 15)),
            "check_in": "09:00:00",
            "check_out": "17:30:00",
            "status": "present",
        }
        response = auth_client.post("/api/attendance/records/", payload)
        assert response.status_code == 201
        assert response.data["status"] == "present"

    def test_create_attendance_check_out_before_check_in_fails(self, auth_client, employee):
        """check_out before check_in triggers validation error."""
        payload = {
            "employee": employee.id,
            "date": str(date(2025, 2, 1)),
            "check_in": "17:00:00",
            "check_out": "09:00:00",
            "status": "present",
        }
        response = auth_client.post("/api/attendance/records/", payload)
        assert response.status_code == 400

    def test_filter_attendance_by_status(self, auth_client, attendance_record):
        """Filter by status returns only matching records."""
        response = auth_client.get("/api/attendance/records/?status=present")
        assert response.status_code == 200
        for record in response.data["results"]:
            assert record["status"] == "present"

    def test_filter_attendance_by_employee(self, auth_client, attendance_record, employee):
        """Filter by employee ID returns only that employee's records."""
        response = auth_client.get(f"/api/attendance/records/?employee={employee.id}")
        assert response.status_code == 200
        assert response.data["count"] >= 1
        for record in response.data["results"]:
            assert record["employee"] == employee.id

    def test_retrieve_attendance_record(self, auth_client, attendance_record):
        """GET detail returns correct attendance record."""
        response = auth_client.get(f"/api/attendance/records/{attendance_record.id}/")
        assert response.status_code == 200
        assert response.data["status"] == attendance_record.status

    def test_attendance_hours_worked(self, auth_client, attendance_record):
        """hours_worked is correctly computed from check_in and check_out."""
        response = auth_client.get(f"/api/attendance/records/{attendance_record.id}/")
        assert response.status_code == 200
        hours = response.data.get("hours_worked")
        assert hours is not None
        assert hours == 8.5

    def test_update_attendance_record(self, auth_client, attendance_record):
        """PATCH updates attendance status."""
        response = auth_client.patch(
            f"/api/attendance/records/{attendance_record.id}/",
            {"status": "remote"},
        )
        assert response.status_code == 200
        assert response.data["status"] == "remote"

    def test_delete_attendance_record(self, auth_client, attendance_record):
        """DELETE removes attendance record and returns 204."""
        response = auth_client.delete(f"/api/attendance/records/{attendance_record.id}/")
        assert response.status_code == 204

    def test_duplicate_attendance_record_fails(self, auth_client, employee, attendance_record):
        """Creating a duplicate (employee, date) pair returns 400."""
        payload = {
            "employee": employee.id,
            "date": str(attendance_record.date),
            "status": "absent",
        }
        response = auth_client.post("/api/attendance/records/", payload)
        assert response.status_code == 400


@pytest.mark.django_db
class TestAttendanceModel:
    """Tests for AttendanceRecord model logic."""

    def test_hours_worked_property(self, attendance_record):
        """hours_worked returns float from check_in to check_out."""
        assert attendance_record.hours_worked == 8.5

    def test_hours_worked_none_when_missing(self, employee, db):
        """hours_worked is None when check_in or check_out is missing."""
        from attendance.models import AttendanceRecord

        record = AttendanceRecord.objects.create(employee=employee, status="absent")
        assert record.hours_worked is None

    def test_str_representation(self, attendance_record):
        """__str__ returns human-readable description."""
        assert "present" in str(attendance_record)
