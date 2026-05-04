"""Custom django-filter FilterSet classes for employee endpoints."""
from __future__ import annotations

import django_filters

from .models import Employee, PerformanceReview


class EmployeeFilter(django_filters.FilterSet):
    """FilterSet for Employee model with range filters."""

    salary_min = django_filters.NumberFilter(field_name="salary", lookup_expr="gte")
    salary_max = django_filters.NumberFilter(field_name="salary", lookup_expr="lte")
    hire_after = django_filters.DateFilter(field_name="hire_date", lookup_expr="gte")
    hire_before = django_filters.DateFilter(field_name="hire_date", lookup_expr="lte")
    name = django_filters.CharFilter(method="filter_by_name")

    class Meta:
        model = Employee
        fields = ["status", "department", "job_title", "salary_min", "salary_max"]

    def filter_by_name(self, queryset, name, value):
        """Filter employees by first or last name (case-insensitive)."""
        from django.db.models import Q

        return queryset.filter(
            Q(first_name__icontains=value) | Q(last_name__icontains=value)
        )


class PerformanceReviewFilter(django_filters.FilterSet):
    """FilterSet for PerformanceReview model with date range filters."""

    review_after = django_filters.DateFilter(field_name="review_date", lookup_expr="gte")
    review_before = django_filters.DateFilter(field_name="review_date", lookup_expr="lte")

    class Meta:
        model = PerformanceReview
        fields = ["employee", "rating", "review_after", "review_before"]
