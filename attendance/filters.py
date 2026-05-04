"""Custom django-filter FilterSet for attendance records."""
from __future__ import annotations

import django_filters

from .models import AttendanceRecord


class AttendanceFilter(django_filters.FilterSet):
    """FilterSet for AttendanceRecord with date range filters."""

    date_after = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_before = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    employee_name = django_filters.CharFilter(method="filter_by_employee_name")

    class Meta:
        model = AttendanceRecord
        fields = ["employee", "status", "date_after", "date_before"]

    def filter_by_employee_name(self, queryset, name, value):
        """Filter records by employee first or last name."""
        from django.db.models import Q

        return queryset.filter(
            Q(employee__first_name__icontains=value)
            | Q(employee__last_name__icontains=value)
        )
