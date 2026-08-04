from __future__ import annotations

import logging
from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        started = perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = (perf_counter() - started) * 1000.0
            request_id = getattr(request.state, "request_id", request.headers.get("x-request-id", ""))
            # Ne journalise jamais la chaîne de requête, qui peut contenir des jetons OAuth.
            logger.info(
                "api_request method=%s path=%s status=%s duration_ms=%.2f request_id=%s client=%s",
                request.method,
                request.url.path,
                status_code,
                duration_ms,
                request_id,
                request.client.host if request.client else "unknown",
            )
