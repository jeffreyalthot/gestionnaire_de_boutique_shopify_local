from __future__ import annotations

import re
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware

_REQUEST_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")


class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        supplied = request.headers.get("X-Request-Id", "").strip()
        request_id = supplied if _REQUEST_ID.fullmatch(supplied) else str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        return response
