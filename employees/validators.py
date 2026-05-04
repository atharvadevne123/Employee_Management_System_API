"""Custom field-level validators for the employees API."""
from __future__ import annotations

import re

from rest_framework.exceptions import ValidationError


def validate_phone_number(value: str) -> str:
    """Validate that the phone number contains only digits, spaces, +, -, and ()."""
    if value and not re.match(r"^[\d\s\+\-\(\)\.]{7,20}$", value):
        raise ValidationError(
            f"'{value}' is not a valid phone number. "
            "Use digits, spaces, +, -, (, ) only."
        )
    return value


def validate_job_title(value: str) -> str:
    """Ensure job title is at least 2 characters and at most 150."""
    value = value.strip()
    if len(value) < 2:
        raise ValidationError("Job title must be at least 2 characters.")
    if len(value) > 150:
        raise ValidationError("Job title must be at most 150 characters.")
    return value


def validate_salary_range(value: float) -> float:
    """Ensure salary is between 0 and 10,000,000."""
    if value < 0:
        raise ValidationError("Salary cannot be negative.")
    if value > 10_000_000:
        raise ValidationError("Salary cannot exceed 10,000,000.")
    return value
