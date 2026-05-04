"""Tests for custom management commands."""
from __future__ import annotations

import pytest
from django.core.management import call_command
from io import StringIO


@pytest.mark.django_db
class TestCreateAdminCommand:
    """Tests for create_admin management command."""

    def test_creates_superuser(self, db):
        """Command creates a superuser when none exists."""
        from django.contrib.auth.models import User

        out = StringIO()
        call_command("create_admin", stdout=out)
        assert User.objects.filter(username="admin", is_superuser=True).exists()

    def test_skips_if_user_exists(self, db):
        """Command skips gracefully if admin user already exists."""
        from django.contrib.auth.models import User

        User.objects.create_superuser(username="admin", email="a@b.com", password="x")
        out = StringIO()
        call_command("create_admin", stdout=out)
        assert User.objects.filter(username="admin").count() == 1


@pytest.mark.django_db
class TestCheckDbCommand:
    """Tests for check_db management command."""

    def test_passes_with_valid_db(self, db):
        """Command exits without error when DB is reachable."""
        out = StringIO()
        call_command("check_db", stdout=out)
        assert "OK" in out.getvalue()


@pytest.mark.django_db
class TestSeedDataCommand:
    """Tests for seed_data management command."""

    def test_creates_employees(self, db):
        """seed_data creates at least 1 employee and department."""
        from employees.models import Department, Employee

        out = StringIO()
        call_command("seed_data", "--count", "5", stdout=out)
        assert Department.objects.count() > 0
        assert Employee.objects.count() >= 5

    def test_clear_flag_removes_existing_data(self, employee, db):
        """--clear removes existing employees before seeding."""
        from employees.models import Employee

        out = StringIO()
        call_command("seed_data", "--count", "3", "--clear", stdout=out)
        assert Employee.objects.count() >= 3
