"""Django admin registration for employees app."""
from __future__ import annotations

from django.contrib import admin

from .models import Department, Employee, PerformanceReview


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin interface for Department model."""

    list_display = ["name", "description", "created_at"]
    search_fields = ["name"]
    ordering = ["name"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin interface for Employee model."""

    list_display = ["full_name", "email", "department", "job_title", "status", "hire_date"]
    list_filter = ["status", "department"]
    search_fields = ["first_name", "last_name", "email"]
    ordering = ["last_name", "first_name"]
    date_hierarchy = "hire_date"


@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    """Admin interface for PerformanceReview model."""

    list_display = ["employee", "reviewer", "review_date", "rating"]
    list_filter = ["rating"]
    search_fields = ["employee__first_name", "employee__last_name", "reviewer"]
    ordering = ["-review_date"]
