"""Tests for Django signals in the employees app."""
from __future__ import annotations

import logging

import pytest


@pytest.mark.django_db
class TestEmployeeSignals:
    """Tests that signals fire correctly on Employee save/delete."""

    def test_create_employee_logs_created(self, department, db, caplog):
        """Creating an employee emits an INFO log via post_save signal."""
        from employees.models import Employee

        with caplog.at_level(logging.INFO, logger="employees"):
            Employee.objects.create(
                first_name="Signal",
                last_name="Test",
                email="signal.test@example.com",
                department=department,
                job_title="Tester",
            )
        assert any("created" in record.message for record in caplog.records)

    def test_delete_employee_logs_deleted(self, employee, caplog):
        """Deleting an employee emits an INFO log via post_delete signal."""
        with caplog.at_level(logging.INFO, logger="employees"):
            employee.delete()
        assert any("deleted" in record.message for record in caplog.records)

    def test_review_save_logs_creation(self, employee, db, caplog):
        """Creating a performance review emits an INFO log."""
        from employees.models import PerformanceReview

        with caplog.at_level(logging.INFO, logger="employees"):
            PerformanceReview.objects.create(
                employee=employee,
                reviewer="Cap Log",
                rating="exceptional",
                comments="Great work.",
            )
        assert any("PerformanceReview created" in record.message for record in caplog.records)
