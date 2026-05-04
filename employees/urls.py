"""URL routing for the employees application."""
from __future__ import annotations

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet,
    EmployeeViewSet,
    PerformanceReviewViewSet,
    health_check,
    version_view,
)

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"employees", EmployeeViewSet, basename="employee")
router.register(r"performance-reviews", PerformanceReviewViewSet, basename="performance-review")

urlpatterns = [
    path("health/", health_check, name="health-check"),
    path("version/", version_view, name="version"),
    *router.urls,
]
