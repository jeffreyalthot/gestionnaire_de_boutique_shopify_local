from __future__ import annotations

import hmac
from collections import defaultdict, deque
from time import monotonic

from fastapi import Header, HTTPException, Request, status


class OperatorAuthorizer:
    """Autorisation locale en temps constant avec protection anti-bruteforce."""

    def __init__(self, settings, *, failure_limit: int = 8, failure_window: float = 60.0) -> None:
        self.settings = settings
        self.failure_limit = max(2, int(failure_limit))
        self.failure_window = max(1.0, float(failure_window))
        self._failures: dict[str, deque[float]] = defaultdict(deque)

    def _host(self, request: Request) -> str:
        return request.client.host if request.client else "unknown"

    def _blocked(self, host: str) -> bool:
        now = monotonic()
        queue = self._failures[host]
        while queue and queue[0] <= now - self.failure_window:
            queue.popleft()
        return len(queue) >= self.failure_limit

    async def require(self, request: Request, x_operator_token: str = Header(default="")) -> None:
        if not self.settings.api_mutations_enabled:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Les mutations API sont désactivées.")
        host = self._host(request)
        if self.settings.api_loopback_only and host not in {"127.0.0.1", "::1", "localhost", "testclient"}:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Mutation limitée à la boucle locale.")
        if self._blocked(host):
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Trop d'échecs d'authentification.")
        expected = self.settings.operator_api_token.get_secret_value()
        supplied = str(x_operator_token)
        valid_shape = 1 <= len(supplied) <= 512
        if not expected or not valid_shape or not hmac.compare_digest(expected.encode("utf-8"), supplied.encode("utf-8")):
            self._failures[host].append(monotonic())
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Jeton opérateur invalide.")
        self._failures.pop(host, None)
