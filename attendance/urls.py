"""URL routing for the attendance application."""
from __future__ import annotations

from rest_framework.routers import DefaultRouter

from .views import AttendanceViewSet

router = DefaultRouter()
router.register(r"records", AttendanceViewSet, basename="attendance")

urlpatterns = router.urls
