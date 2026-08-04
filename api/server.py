from fastapi import FastAPI
from api.router import build_router
from api.exception_handlers import unhandled_exception_handler
from api.middleware.request_id import RequestIdMiddleware
from api.middleware.security_headers import SecurityHeadersMiddleware
from api.middleware.request_logging import RequestLoggingMiddleware
from api.middleware.body_size_limit import BodySizeLimitMiddleware
from api.middleware.rate_limiter import RateLimiterMiddleware
from app.version import VERSION

def create_app(container) -> FastAPI:
    app=FastAPI(title="Shopify–Alibaba AI Orchestrator",version=VERSION,docs_url="/docs",redoc_url="/redoc")
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(BodySizeLimitMiddleware,maximum_bytes=2_000_000)
    app.add_middleware(RateLimiterMiddleware,limit=240,window=60)
    app.include_router(build_router(container))
    app.add_exception_handler(Exception,unhandled_exception_handler)
    return app
