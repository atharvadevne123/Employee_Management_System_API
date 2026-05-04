"""App configuration for employees."""
from __future__ import annotations

from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    """Configuration for the employees Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "employees"

    def ready(self) -> None:
        """Perform app initialization on startup."""
