"""Utility functions for the employees application."""
from __future__ import annotations

import functools
import logging
from typing import Any

logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=128)
def get_rating_display_map() -> dict[str, str]:
    """Return cached mapping of rating codes to display labels."""
    from .models import PerformanceReview

    return dict(PerformanceReview.RATING_CHOICES)


@functools.lru_cache(maxsize=32)
def get_status_display_map() -> dict[str, str]:
    """Return cached mapping of employment status codes to display labels."""
    from .models import Employee

    return dict(Employee.EMPLOYMENT_STATUS_CHOICES)


def build_employee_summary(employee_id: int) -> dict[str, Any]:
    """Build a summary dict for an employee including latest review rating.

    Returns an empty dict if the employee does not exist.
    """
    try:
        from .models import Employee

        emp = Employee.objects.select_related("department").get(pk=employee_id)
        latest_review = emp.performance_reviews.first()
        return {
            "id": emp.id,
            "full_name": emp.full_name,
            "department": str(emp.department) if emp.department else None,
            "status": emp.status,
            "latest_rating": latest_review.rating if latest_review else None,
        }
    except Exception as exc:
        logger.warning("Could not build summary for employee %s: %s", employee_id, exc)
        return {}
