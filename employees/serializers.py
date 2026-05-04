"""DRF serializers for employees, departments, and performance reviews."""
from __future__ import annotations

from rest_framework import serializers

from .models import Department, Employee, PerformanceReview


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for Department model with employee count."""

    employee_count = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "description", "employee_count", "created_at"]
        read_only_fields = ["id", "created_at"]

    def get_employee_count(self, obj: Department) -> int:
        """Return the number of active employees in this department."""
        return obj.employees.filter(status="active").count()


class PerformanceReviewSerializer(serializers.ModelSerializer):
    """Serializer for PerformanceReview model."""

    employee_name = serializers.CharField(source="employee.full_name", read_only=True)

    class Meta:
        model = PerformanceReview
        fields = [
            "id",
            "employee",
            "employee_name",
            "reviewer",
            "review_date",
            "rating",
            "comments",
            "goals",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "employee_name"]


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model with nested department info."""

    department_name = serializers.CharField(
        source="department.name", read_only=True, default=""
    )
    full_name = serializers.CharField(read_only=True)
    performance_reviews = PerformanceReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "phone",
            "department",
            "department_name",
            "job_title",
            "salary",
            "hire_date",
            "status",
            "performance_reviews",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "full_name", "created_at", "updated_at"]

    def validate_email(self, value: str) -> str:
        """Ensure email is lowercase and unique (case-insensitive)."""
        return value.lower()

    def validate_salary(self, value: float) -> float:
        """Ensure salary is non-negative."""
        if value < 0:
            raise serializers.ValidationError("Salary cannot be negative.")
        return value


class EmployeeListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing employees (without nested reviews)."""

    department_name = serializers.CharField(
        source="department.name", read_only=True, default=""
    )
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "full_name",
            "email",
            "department_name",
            "job_title",
            "status",
            "hire_date",
        ]
