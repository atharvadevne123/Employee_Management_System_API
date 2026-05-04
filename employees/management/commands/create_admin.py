"""Management command to create a default admin superuser for development."""
from __future__ import annotations

import logging
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Create a default superuser if one does not already exist."""

    help = "Create a default admin superuser for development"

    def handle(self, *args, **options) -> None:
        """Create admin user if not present."""
        username = os.environ.get("ADMIN_USERNAME", "admin")
        email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
        password = os.environ.get("ADMIN_PASSWORD", "adminpass123")

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"Admin user '{username}' already exists.")
            return

        try:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
            self.stdout.write(
                self.style.SUCCESS(f"Admin user '{username}' created successfully.")
            )
            logger.info("Admin user created: %s", username)
        except Exception as exc:
            logger.error("Failed to create admin user: %s", exc)
            self.stderr.write(str(exc))
