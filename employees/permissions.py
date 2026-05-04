"""Custom DRF permission classes for the employees API."""
from __future__ import annotations

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminOrReadOnly(BasePermission):
    """Allow safe (GET, HEAD, OPTIONS) requests to any authenticated user.

    Mutating requests (POST, PUT, PATCH, DELETE) require is_staff=True.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return True for safe methods; require admin for mutations."""
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


class IsSelfOrAdmin(BasePermission):
    """Allow users to read their own records; admins can access all records."""

    def has_object_permission(self, request: Request, view: APIView, obj) -> bool:
        """Return True if user owns the object or is staff."""
        if request.user and request.user.is_staff:
            return True
        if hasattr(obj, "email"):
            return obj.email == request.user.email
        if hasattr(obj, "employee"):
            return obj.employee.email == request.user.email
        return False
