from __future__ import annotations

import uuid
from time import monotonic

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class ExceptionGuardMiddleware(BaseHTTPMiddleware):
    """Convertit les exceptions non gérées en réponses sûres sans exposer de secrets."""

    async def dispatch(self, request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        started = monotonic()
        try:
            response = await call_next(request)
        except (ValueError, KeyError) as exc:
            response = JSONResponse(
                {"error": "invalid_request", "request_id": request_id, "detail": str(exc)[:300]},
                status_code=400,
            )
        except PermissionError:
            response = JSONResponse({"error": "forbidden", "request_id": request_id}, status_code=403)
        except TimeoutError:
            response = JSONResponse({"error": "timeout", "request_id": request_id}, status_code=504)
        except Exception:
            response = JSONResponse({"error": "internal_error", "request_id": request_id}, status_code=500)
        response.headers["x-request-id"] = request_id
        response.headers["server-timing"] = f"app;dur={(monotonic() - started) * 1000:.2f}"
        return response
