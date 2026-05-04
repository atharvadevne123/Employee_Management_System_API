"""Django ORM models for employees, departments, and performance reviews."""
from __future__ import annotations

import logging
from datetime import date
from typing import ClassVar

from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


class Department(models.Model):
    """Organisational department that groups employees."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering: ClassVar[list[str]] = ["name"]

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    """Core employee record linked to a department."""

    EMPLOYMENT_STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("on_leave", "On Leave"),
        ("terminated", "Terminated"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, default="")
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
    )
    job_title = models.CharField(max_length=150)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hire_date = models.DateField(default=date.today)
    status = models.CharField(
        max_length=20, choices=EMPLOYMENT_STATUS_CHOICES, default="active"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ClassVar[list[str]] = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self) -> str:
        """Return the employee's full name."""
        return f"{self.first_name} {self.last_name}"


class PerformanceReview(models.Model):
    """Annual or periodic performance review for an employee."""

    RATING_CHOICES: ClassVar[list[tuple[str, str]]] = [
        ("exceptional", "Exceptional"),
        ("exceeds_expectations", "Exceeds Expectations"),
        ("meets_expectations", "Meets Expectations"),
        ("needs_improvement", "Needs Improvement"),
        ("unsatisfactory", "Unsatisfactory"),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="performance_reviews"
    )
    reviewer = models.CharField(max_length=200)
    review_date = models.DateField(default=date.today)
    rating = models.CharField(max_length=30, choices=RATING_CHOICES)
    comments = models.TextField(blank=True, default="")
    goals = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering: ClassVar[list[str]] = ["-review_date"]

    def __str__(self) -> str:
        return f"Review for {self.employee} on {self.review_date}"
