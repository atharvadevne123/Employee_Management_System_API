"""App configuration for attendance."""
from __future__ import annotations

from django.apps import AppConfig


class AttendanceConfig(AppConfig):
    """Configuration for the attendance Django application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "attendance"
