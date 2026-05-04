"""Tests for Django ORM models."""
from __future__ import annotations

import pytest


@pytest.mark.django_db
class TestDepartmentModel:
    """Tests for the Department model."""

    def test_str_representation(self, department):
        """Department __str__ returns department name."""
        assert str(department) == department.name

    def test_default_ordering(self, db):
        """Departments are ordered alphabetically by name."""
        from employees.models import Department

        Department.objects.create(name="Zebra Dept")
        Department.objects.create(name="Alpha Dept")
        names = list(Department.objects.values_list("name", flat=True))
        assert names == sorted(names)

    def test_unique_name_constraint(self, department, db):
        """Creating two departments with the same name raises IntegrityError."""
        from django.db import IntegrityError

        with pytest.raises(IntegrityError):
            from employees.models import Department

            Department.objects.create(name=department.name)


@pytest.mark.django_db
class TestEmployeeModel:
    """Tests for the Employee model."""

    def test_full_name_property(self, employee):
        """full_name concatenates first and last name."""
        assert employee.full_name == "Jane Doe"

    def test_str_representation(self, employee):
        """Employee __str__ returns full name."""
        assert str(employee) == "Jane Doe"

    def test_unique_email_constraint(self, employee, department, db):
        """Two employees cannot share the same email address."""
        from django.db import IntegrityError

        from employees.models import Employee

        with pytest.raises(IntegrityError):
            Employee.objects.create(
                first_name="Duplicate",
                last_name="User",
                email=employee.email,
                department=department,
                job_title="Engineer",
            )

    def test_status_defaults_to_active(self, department, db):
        """Newly created employee has status='active' by default."""
        from employees.models import Employee

        emp = Employee.objects.create(
            first_name="New",
            last_name="Hire",
            email="new.hire@example.com",
            department=department,
            job_title="Intern",
        )
        assert emp.status == "active"

    def test_salary_default_is_zero(self, department, db):
        """Default salary is 0 when not specified."""
        from employees.models import Employee

        emp = Employee.objects.create(
            first_name="Test",
            last_name="User",
            email="test.user@example.com",
            department=department,
            job_title="Contractor",
        )
        assert emp.salary == 0


@pytest.mark.django_db
class TestPerformanceReviewModel:
    """Tests for the PerformanceReview model."""

    def test_str_representation(self, performance_review, employee):
        """PerformanceReview __str__ contains employee name and date."""
        result = str(performance_review)
        assert "Jane Doe" in result

    def test_review_linked_to_employee(self, performance_review, employee):
        """Review's employee FK points to correct employee."""
        assert performance_review.employee_id == employee.id

    def test_default_ordering_is_newest_first(self, employee, db):
        """Reviews are ordered by -review_date (newest first)."""
        from datetime import date

        from employees.models import PerformanceReview

        PerformanceReview.objects.create(
            employee=employee,
            reviewer="Rev A",
            review_date=date(2023, 1, 1),
            rating="meets_expectations",
        )
        PerformanceReview.objects.create(
            employee=employee,
            reviewer="Rev B",
            review_date=date(2024, 6, 15),
            rating="exceptional",
        )
        dates = list(
            employee.performance_reviews.values_list("review_date", flat=True)
        )
        assert dates == sorted(dates, reverse=True)
