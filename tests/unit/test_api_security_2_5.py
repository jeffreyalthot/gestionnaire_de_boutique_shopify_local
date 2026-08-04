from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from api.exception_handlers import unhandled_exception_handler
from api.middleware.body_size_limit import BodySizeLimitMiddleware
from api.middleware.rate_limiter import RateLimiterMiddleware
from api.middleware.request_id import RequestIdMiddleware
from api.middleware.security_headers import SecurityHeadersMiddleware
from api.request_context import RequestContext


def _app(*middlewares):
    app = FastAPI()
    for middleware, kwargs in middlewares:
        app.add_middleware(middleware, **kwargs)

    @app.post("/echo")
    async def echo(request: Request):
        body = await request.body()
        return {"length": len(body), "request_id": getattr(request.state, "request_id", "")}

    @app.get("/boom")
    async def boom():
        raise RuntimeError("sensitive internal detail")

    app.add_exception_handler(Exception, unhandled_exception_handler)
    return app


def test_body_size_limit_rejects_actual_body():
    client = TestClient(_app((BodySizeLimitMiddleware, {"maximum_bytes": 4})), raise_server_exceptions=False)
    assert client.post("/echo", content=b"1234").status_code == 200
    response = client.post("/echo", content=b"12345")
    assert response.status_code == 413 and response.json()["error"] == "request_body_too_large"


def test_request_id_accepts_safe_and_replaces_unsafe():
    client = TestClient(_app((RequestIdMiddleware, {})))
    safe = client.post("/echo", headers={"X-Request-Id": "job-1"})
    assert safe.headers["X-Request-Id"] == "job-1" and safe.json()["request_id"] == "job-1"
    unsafe = client.post("/echo", headers={"X-Request-Id": "bad id\n"})
    assert unsafe.headers["X-Request-Id"] != "bad id\n"


def test_rate_limiter_sets_headers_and_retries():
    client = TestClient(_app((RateLimiterMiddleware, {"limit": 2, "window": 60, "exempt_paths": ()})))
    assert client.post("/echo").headers["X-RateLimit-Remaining"] == "1"
    assert client.post("/echo").headers["X-RateLimit-Remaining"] == "0"
    limited = client.post("/echo")
    assert limited.status_code == 429 and int(limited.headers["Retry-After"]) >= 1


def test_security_headers_are_present():
    client = TestClient(_app((SecurityHeadersMiddleware, {})))
    response = client.post("/echo")
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert "camera=()" in response.headers["Permissions-Policy"]
    assert response.headers["Cache-Control"].startswith("no-store")


def test_exception_handler_hides_internal_message():
    client = TestClient(_app((RequestIdMiddleware, {})), raise_server_exceptions=False)
    response = client.get("/boom")
    assert response.status_code == 500
    assert response.json()["error"] == "internal_error"
    assert "sensitive" not in response.text
    assert response.json()["request_id"] == response.headers["X-Request-Id"]


def test_request_context_normalizes_fields():
    context = RequestContext("r1", actor="operator", method="post", shop_domain="EXAMPLE.MYSHOPIFY.COM")
    assert context.method == "POST" and context.shop_domain == "example.myshopify.com"
    assert context.as_dict()["request_id"] == "r1"
