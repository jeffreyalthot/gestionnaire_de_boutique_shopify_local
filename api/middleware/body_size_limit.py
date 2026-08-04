from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    """Refuse les corps annoncés ou observés au-delà de la limite configurée."""

    def __init__(self, app, maximum_bytes: int = 2_000_000) -> None:
        super().__init__(app)
        self.maximum = max(1, int(maximum_bytes))
        self.rejected = 0

    async def dispatch(self, request, call_next):
        header = request.headers.get("content-length", "").strip()
        if header:
            try:
                length = int(header)
            except ValueError:
                self.rejected += 1
                return JSONResponse({"error": "invalid_content_length"}, status_code=400)
            if length < 0:
                self.rejected += 1
                return JSONResponse({"error": "invalid_content_length"}, status_code=400)
            if length > self.maximum:
                self.rejected += 1
                return JSONResponse({"error": "request_body_too_large", "maximum_bytes": self.maximum}, status_code=413)

        body = await request.body()
        if len(body) > self.maximum:
            self.rejected += 1
            return JSONResponse({"error": "request_body_too_large", "maximum_bytes": self.maximum}, status_code=413)
        return await call_next(request)
