from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, *, hsts: bool = False) -> None:
        super().__init__(app)
        self.hsts = bool(hsts)

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
            "Cache-Control": "no-store, max-age=0",
            "Pragma": "no-cache",
            "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()",
            "Content-Security-Policy": "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'",
            "Cross-Origin-Resource-Policy": "same-origin",
        }
        if self.hsts and request.url.scheme == "https":
            headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        for key, value in headers.items():
            response.headers.setdefault(key, value)
        return response
