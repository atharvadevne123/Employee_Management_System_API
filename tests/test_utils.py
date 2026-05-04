"""Tests for employees.utils module."""
from __future__ import annotations

import pytest


@pytest.mark.django_db
class TestGetRatingDisplayMap:
    """Tests for get_rating_display_map utility."""

    def test_returns_dict(self):
        """Function returns a dictionary."""
        from employees.utils import get_rating_display_map

        result = get_rating_display_map()
        assert isinstance(result, dict)

    def test_contains_expected_ratings(self):
        """Expected rating keys are present in the map."""
        from employees.utils import get_rating_display_map

        result = get_rating_display_map()
        assert "exceptional" in result
        assert "meets_expectations" in result
        assert "needs_improvement" in result

    def test_is_cached(self):
        """Calling twice returns the same object (cached)."""
        from employees.utils import get_rating_display_map

        a = get_rating_display_map()
        b = get_rating_display_map()
        assert a is b


@pytest.mark.django_db
class TestBuildEmployeeSummary:
    """Tests for build_employee_summary utility."""

    def test_returns_summary_for_valid_employee(self, employee):
        """Returns dict with expected keys for a valid employee."""
        from employees.utils import build_employee_summary

        result = build_employee_summary(employee.id)
        assert result["id"] == employee.id
        assert result["full_name"] == employee.full_name
        assert "status" in result
        assert "latest_rating" in result

    def test_returns_empty_dict_for_invalid_id(self):
        """Returns empty dict for non-existent employee ID."""
        from employees.utils import build_employee_summary

        result = build_employee_summary(999999)
        assert result == {}

    def test_latest_rating_is_none_without_reviews(self, employee):
        """latest_rating is None when employee has no reviews."""
        from employees.utils import build_employee_summary

        result = build_employee_summary(employee.id)
        assert result["latest_rating"] is None

    def test_latest_rating_present_with_review(self, employee, performance_review):
        """latest_rating is set when a review exists."""
        from employees.utils import build_employee_summary

        result = build_employee_summary(employee.id)
        assert result["latest_rating"] == performance_review.rating
