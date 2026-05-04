"""API views for attendance records."""
from __future__ import annotations

import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer

logger = logging.getLogger(__name__)


class AttendanceViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for employee attendance records."""

    queryset = AttendanceRecord.objects.select_related("employee")
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["employee", "status", "date"]
    search_fields = ["employee__first_name", "employee__last_name", "notes"]
    ordering_fields = ["date", "check_in", "created_at"]
    ordering = ["-date"]

    def perform_create(self, serializer: AttendanceRecordSerializer) -> None:
        """Log attendance record creation."""
        instance = serializer.save()
        logger.info(
            "Attendance record created: employee=%s date=%s status=%s",
            instance.employee_id,
            instance.date,
            instance.status,
        )

    def perform_update(self, serializer: AttendanceRecordSerializer) -> None:
        """Log attendance record update."""
        instance = serializer.save()
        logger.info(
            "Attendance record updated: id=%s employee=%s",
            instance.id,
            instance.employee_id,
        )
