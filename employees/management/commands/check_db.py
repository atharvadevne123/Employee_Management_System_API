"""Management command to verify database connectivity."""
from __future__ import annotations

import logging
import sys

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Probe the default database connection and exit non-zero on failure."""

    help = "Check database connectivity — exits 1 if DB is unreachable"

    def handle(self, *args, **options) -> None:
        """Attempt a lightweight DB query to confirm connectivity."""
        try:
            conn = connections["default"]
            conn.ensure_connection()
            self.stdout.write(self.style.SUCCESS("Database connection OK."))
            logger.info("Database health check passed.")
        except OperationalError as exc:
            logger.error("Database health check failed: %s", exc)
            self.stderr.write(self.style.ERROR(f"Database connection FAILED: {exc}"))
            sys.exit(1)
