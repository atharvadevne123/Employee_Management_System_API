"""Django ORM model for employee attendance records."""
from __future__ import annotations

import logging
from typing import ClassVar

from django.db import models
from django.utils import timezone

from employees.models import Employee

logger = logging.getLogger(__name__)


class AttendanceRecord(models.Model):
    """Daily attendance record for a single employee."""

    STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
        ("half_day", "Half Day"),
        ("remote", "Remote"),
        ("on_leave", "On Leave"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="attendance_records",
    )
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="present")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["-date"]
        unique_together: ClassVar[list[list[str]]] = [["employee", "date"]]

    def __str__(self) -> str:
        return f"{self.employee} — {self.date} ({self.status})"

    @property
    def hours_worked(self) -> float | None:
        """Calculate hours worked from check_in and check_out times."""
        if self.check_in and self.check_out:
            from datetime import datetime, date as dt_date

            base = dt_date.today()
            ci = datetime.combine(base, self.check_in)
            co = datetime.combine(base, self.check_out)
            delta = co - ci
            if delta.total_seconds() > 0:
                return round(delta.total_seconds() / 3600, 2)
        return None
