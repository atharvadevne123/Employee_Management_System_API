"""API views for employees, departments, and performance reviews."""
from __future__ import annotations

import logging

from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .filters import EmployeeFilter, PerformanceReviewFilter
from .models import Department, Employee, PerformanceReview
from .serializers import (
    DepartmentSerializer,
    EmployeeListSerializer,
    EmployeeSerializer,
    PerformanceReviewSerializer,
)

logger = logging.getLogger(__name__)


class DepartmentViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for organisational departments."""

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def perform_create(self, serializer: DepartmentSerializer) -> None:
        """Log department creation."""
        instance = serializer.save()
        logger.info("Department created: %s (id=%s)", instance.name, instance.id)

    def perform_destroy(self, instance: Department) -> None:
        """Log department deletion."""
        logger.info("Department deleted: %s (id=%s)", instance.name, instance.id)
        instance.delete()


class EmployeeViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for employee records."""

    queryset = Employee.objects.select_related("department").prefetch_related(
        "performance_reviews"
    )
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EmployeeFilter
    search_fields = ["first_name", "last_name", "email", "job_title"]
    ordering_fields = ["last_name", "hire_date", "salary", "created_at"]
    ordering = ["last_name"]

    def get_serializer_class(self):
        """Use lightweight serializer for list actions."""
        if self.action == "list":
            return EmployeeListSerializer
        return EmployeeSerializer

    def perform_create(self, serializer: EmployeeSerializer) -> None:
        """Log employee creation."""
        instance = serializer.save()
        logger.info(
            "Employee created: %s (id=%s, dept=%s)",
            instance.full_name,
            instance.id,
            instance.department,
        )

    def perform_update(self, serializer: EmployeeSerializer) -> None:
        """Log employee update."""
        instance = serializer.save()
        logger.info("Employee updated: %s (id=%s)", instance.full_name, instance.id)

    def perform_destroy(self, instance: Employee) -> None:
        """Log employee deletion."""
        logger.info("Employee deleted: %s (id=%s)", instance.full_name, instance.id)
        instance.delete()

    @action(detail=True, methods=["get"], url_path="reviews")
    def reviews(self, request: Request, pk: int | None = None) -> Response:
        """Return all performance reviews for a specific employee."""
        employee = self.get_object()
        reviews = employee.performance_reviews.all()
        serializer = PerformanceReviewSerializer(reviews, many=True)
        logger.debug("Fetched %d reviews for employee %s", len(reviews), pk)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="by-department")
    def by_department(self, request: Request) -> Response:
        """Return employee counts grouped by department."""
        from django.db.models import Count

        data = (
            Department.objects.annotate(count=Count("employees"))
            .values("id", "name", "count")
            .order_by("name")
        )
        return Response(list(data))


class PerformanceReviewViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for employee performance reviews."""

    queryset = PerformanceReview.objects.select_related("employee")
    serializer_class = PerformanceReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PerformanceReviewFilter
    search_fields = ["reviewer", "comments"]
    ordering_fields = ["review_date", "created_at"]
    ordering = ["-review_date"]

    def perform_create(self, serializer: PerformanceReviewSerializer) -> None:
        """Log review creation."""
        instance = serializer.save()
        logger.info(
            "Performance review created for employee %s (rating=%s)",
            instance.employee_id,
            instance.rating,
        )


def health_check(request: Request) -> JsonResponse:
    """Liveness probe endpoint — returns 200 when the app is running."""
    return JsonResponse({"status": "ok", "service": "employee-management-api"})


def version_view(request: Request) -> JsonResponse:
    """Return current API version."""
    return JsonResponse({"version": "1.0.0", "api": "v1"})
