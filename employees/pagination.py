"""Custom pagination classes for the employees API."""
from __future__ import annotations

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsPagination(PageNumberPagination):
    """Default pagination: 20 items per page, configurable via query param."""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 200

    def get_paginated_response(self, data) -> Response:
        """Return response with pagination metadata."""
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "results": data,
            }
        )


class LargeResultsPagination(PageNumberPagination):
    """Pagination for bulk exports: 100 items per page."""

    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000
