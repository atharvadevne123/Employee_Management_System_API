"""Django signals for the employees application."""
from __future__ import annotations

import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Employee, PerformanceReview

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Employee)
def log_employee_save(sender, instance: Employee, created: bool, **kwargs) -> None:
    """Log when an employee record is created or updated."""
    action = "created" if created else "updated"
    logger.info(
        "Employee %s: id=%s name=%s dept=%s status=%s",
        action,
        instance.id,
        instance.full_name,
        instance.department,
        instance.status,
    )


@receiver(post_delete, sender=Employee)
def log_employee_delete(sender, instance: Employee, **kwargs) -> None:
    """Log when an employee record is deleted."""
    logger.info(
        "Employee deleted: id=%s name=%s",
        instance.id,
        instance.full_name,
    )


@receiver(post_save, sender=PerformanceReview)
def log_review_save(sender, instance: PerformanceReview, created: bool, **kwargs) -> None:
    """Log when a performance review is created."""
    if created:
        logger.info(
            "PerformanceReview created: employee=%s rating=%s reviewer=%s",
            instance.employee_id,
            instance.rating,
            instance.reviewer,
        )
