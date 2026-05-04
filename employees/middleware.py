"""Custom Django middleware for the employees API."""
from __future__ import annotations

import logging
import time
import uuid

from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    """Attach a unique X-Request-ID header to every response for tracing."""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.request_id = request_id
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        return response


class RequestLoggingMiddleware:
    """Log method, path, status code, and duration for every request."""

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = round((time.perf_counter() - start) * 1000, 1)
        request_id = getattr(request, "request_id", "-")
        logger.info(
            "%s %s %s %.1fms rid=%s",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
            request_id,
        )
        return response
