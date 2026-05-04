"""Tests for custom validators."""
from __future__ import annotations

import pytest
from rest_framework.exceptions import ValidationError

from employees.validators import (
    validate_job_title,
    validate_phone_number,
    validate_salary_range,
)


class TestPhoneValidator:
    """Tests for validate_phone_number."""

    def test_valid_phone_passes(self):
        """Valid phone number passes without error."""
        assert validate_phone_number("555-1234") == "555-1234"

    def test_valid_international_phone_passes(self):
        """+1 international format passes."""
        assert validate_phone_number("+1 (555) 123-4567") == "+1 (555) 123-4567"

    def test_empty_string_passes(self):
        """Empty string (optional field) passes validation."""
        assert validate_phone_number("") == ""

    def test_invalid_phone_raises(self):
        """Phone with invalid characters raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_phone_number("abc-def-ghij")

    def test_too_short_phone_raises(self):
        """Phone shorter than 7 characters raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_phone_number("123")


class TestJobTitleValidator:
    """Tests for validate_job_title."""

    def test_valid_title_passes(self):
        """Standard job title passes."""
        assert validate_job_title("  Software Engineer  ") == "Software Engineer"

    def test_too_short_raises(self):
        """Single-character title raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_job_title("A")

    def test_too_long_raises(self):
        """Title over 150 characters raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_job_title("X" * 151)

    def test_whitespace_stripped(self):
        """Surrounding whitespace is stripped before validation."""
        result = validate_job_title("  Dev  ")
        assert result == "Dev"


class TestSalaryValidator:
    """Tests for validate_salary_range."""

    def test_valid_salary_passes(self):
        """Normal salary passes."""
        assert validate_salary_range(75000) == 75000

    def test_zero_salary_passes(self):
        """Zero salary is valid."""
        assert validate_salary_range(0) == 0

    def test_negative_salary_raises(self):
        """Negative salary raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_salary_range(-1)

    def test_excessive_salary_raises(self):
        """Salary above 10M raises ValidationError."""
        with pytest.raises(ValidationError):
            validate_salary_range(10_000_001)

    def test_max_valid_salary(self):
        """Exactly 10M passes."""
        assert validate_salary_range(10_000_000) == 10_000_000
