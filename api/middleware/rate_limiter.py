from __future__ import annotations

from collections import OrderedDict, deque
from threading import RLock
from time import monotonic
from typing import Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Fenêtre glissante bornée en mémoire, adaptée à un service local 2 Go."""

    def __init__(
        self,
        app,
        limit: int = 120,
        window: float = 60.0,
        *,
        maximum_clients: int = 4096,
        exempt_paths: tuple[str, ...] = ("/health/live",),
    ) -> None:
        super().__init__(app)
        self.limit = max(1, int(limit))
        self.window = max(0.1, float(window))
        self.maximum_clients = max(16, int(maximum_clients))
        self.exempt_paths = frozenset(exempt_paths)
        self.hits: OrderedDict[str, deque[float]] = OrderedDict()
        self._lock = RLock()
        self.allowed = 0
        self.rejected = 0

    @staticmethod
    def _client_key(request: Any) -> str:
        client = request.client.host if request.client else "unknown"
        token = request.headers.get("x-operator-id", "").strip()
        return f"{client}:{token[:64]}" if token else client

    def _check(self, key: str, now: float) -> tuple[bool, int, float]:
        with self._lock:
            queue = self.hits.pop(key, deque())
            cutoff = now - self.window
            while queue and queue[0] <= cutoff:
                queue.popleft()
            if len(queue) >= self.limit:
                retry_after = max(0.1, queue[0] + self.window - now)
                self.hits[key] = queue
                self.rejected += 1
                return False, 0, retry_after
            queue.append(now)
            self.hits[key] = queue
            while len(self.hits) > self.maximum_clients:
                self.hits.popitem(last=False)
            self.allowed += 1
            return True, max(0, self.limit - len(queue)), 0.0

    async def dispatch(self, request, call_next):
        if request.url.path in self.exempt_paths:
            return await call_next(request)
        allowed, remaining, retry_after = self._check(self._client_key(request), monotonic())
        if not allowed:
            return JSONResponse(
                {"error": "rate_limit_exceeded"},
                status_code=429,
                headers={"Retry-After": str(max(1, int(retry_after + 0.999)))},
            )
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.limit)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        return response

    def statistics(self) -> dict[str, int | float]:
        with self._lock:
            return {
                "limit": self.limit,
                "window_seconds": self.window,
                "tracked_clients": len(self.hits),
                "allowed": self.allowed,
                "rejected": self.rejected,
            }
