from __future__ import annotations

from uuid import uuid4

from fastapi import Request
from fastapi.responses import JSONResponse


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Retourne une erreur corrélable sans exposer le message interne."""
    request_id = getattr(request.state, "request_id", request.headers.get("x-request-id", "")) or str(uuid4())
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "request_id": request_id, "path": request.url.path},
        headers={"X-Request-Id": request_id, "Cache-Control": "no-store"},
    )
