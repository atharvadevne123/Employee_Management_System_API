"""Custom exception handler for the employees API."""
from __future__ import annotations

import logging

from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc: Exception, context: dict) -> Response | None:
    """Wrap DRF default exception handler to add request_id and log errors."""
    response = exception_handler(exc, context)

    if isinstance(exc, DjangoValidationError):
        response = Response(
            {"detail": exc.messages},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if response is not None:
        if response.status_code >= 500:
            logger.error(
                "Server error %s: %s",
                response.status_code,
                exc,
                exc_info=True,
            )
        elif response.status_code >= 400:
            logger.warning("Client error %s: %s", response.status_code, exc)

        response.data["status_code"] = response.status_code

    return response


class ServiceUnavailableError(APIException):
    """Raised when a downstream service is temporarily unavailable."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Service temporarily unavailable. Try again later."
    default_code = "service_unavailable"
