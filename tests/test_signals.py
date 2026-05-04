"""Tests for Django signals in the employees app."""
from __future__ import annotations

from unittest.mock import patch

import pytest


@pytest.mark.django_db
class TestEmployeeSignals:
    """Tests that signals fire correctly on Employee save/delete."""

    def test_post_save_signal_fires_on_create(self, department, db):
        """post_save signal fires when an employee is created."""
        from employees.models import Employee

        signal_received = []

        from django.db.models.signals import post_save

        def handler(sender, instance, created, **kwargs):
            if created:
                signal_received.append(instance.full_name)

        post_save.connect(handler, sender=Employee)
        try:
            Employee.objects.create(
                first_name="Signal",
                last_name="Test",
                email="signal.test@example.com",
                department=department,
                job_title="Tester",
            )
            assert len(signal_received) == 1
            assert signal_received[0] == "Signal Test"
        finally:
            post_save.disconnect(handler, sender=Employee)

    def test_post_delete_signal_fires_on_delete(self, employee, db):
        """post_delete signal fires when an employee is deleted."""
        from employees.models import Employee

        deleted_ids = []

        from django.db.models.signals import post_delete

        def handler(sender, instance, **kwargs):
            deleted_ids.append(instance.id)

        emp_id = employee.id
        post_delete.connect(handler, sender=Employee)
        try:
            employee.delete()
            assert emp_id in deleted_ids
        finally:
            post_delete.disconnect(handler, sender=Employee)

    def test_review_post_save_signal_fires(self, employee, db):
        """post_save signal fires when a performance review is created."""
        from employees.models import PerformanceReview

        saved = []

        from django.db.models.signals import post_save

        def handler(sender, instance, created, **kwargs):
            if created:
                saved.append(instance.rating)

        post_save.connect(handler, sender=PerformanceReview)
        try:
            PerformanceReview.objects.create(
                employee=employee,
                reviewer="Cap Log",
                rating="exceptional",
                comments="Great work.",
            )
            assert "exceptional" in saved
        finally:
            post_save.disconnect(handler, sender=PerformanceReview)

    def test_log_employee_save_logs_with_mock(self, department, db):
        """Signal log_employee_save calls logger.info on create."""
        from employees import signals
        from employees.models import Employee

        with patch.object(signals.logger, "info") as mock_log:
            Employee.objects.create(
                first_name="Mock",
                last_name="Log",
                email="mock.log@example.com",
                department=department,
                job_title="Mocker",
            )
            assert mock_log.called
