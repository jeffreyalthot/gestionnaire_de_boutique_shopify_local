from __future__ import annotations

from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any, Mapping

import httpx

from infrastructure.http.tls import secure_ssl_context


@dataclass(frozen=True, slots=True)
class ClientConfiguration:
    timeout_seconds: float
    connect_timeout_seconds: float
    max_connections: int
    max_keepalive_connections: int
    keepalive_expiry_seconds: float
    follow_redirects: bool
    http2: bool
    trust_env: bool

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ClientMetrics:
    requests: int = 0
    failures: int = 0
    bytes_received: int = 0
    total_duration_seconds: float = 0.0

    def snapshot(self) -> dict[str, Any]:
        average = self.total_duration_seconds / self.requests if self.requests else 0.0
        return {
            "requests": self.requests,
            "failures": self.failures,
            "bytes_received": self.bytes_received,
            "average_duration_seconds": round(average, 6),
        }


def create_async_client(
    timeout: float,
    max_connections: int = 10,
    *,
    max_keepalive_connections: int | None = None,
    connect_timeout: float | None = None,
    keepalive_expiry: float = 15.0,
    follow_redirects: bool = True,
    http2: bool = False,
    trust_env: bool = False,
    headers: Mapping[str, str] | None = None,
) -> httpx.AsyncClient:
    """Crée un client faible mémoire avec limites explicites et TLS vérifié."""
    timeout_value = max(0.1, float(timeout))
    maximum = max(1, int(max_connections))
    keepalive = max(0, min(maximum, int(max_keepalive_connections if max_keepalive_connections is not None else maximum)))
    limits = httpx.Limits(
        max_connections=maximum,
        max_keepalive_connections=keepalive,
        keepalive_expiry=max(0.0, float(keepalive_expiry)),
    )
    timeout_config = httpx.Timeout(
        timeout_value,
        connect=max(0.1, float(connect_timeout if connect_timeout is not None else min(timeout_value, 10.0))),
    )
    default_headers = {"User-Agent": "Shopify-Alibaba-Orchestrator/2.5", "Accept": "application/json"}
    default_headers.update(dict(headers or {}))
    return httpx.AsyncClient(
        timeout=timeout_config,
        limits=limits,
        follow_redirects=bool(follow_redirects),
        http2=bool(http2),
        trust_env=bool(trust_env),
        verify=secure_ssl_context(),
        headers=default_headers,
    )


class ManagedAsyncClient:
    """Façade instrumentée conservant l'API httpx pour les appels métier."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client
        self.metrics = ClientMetrics()

    async def request(self, method: str, url: str, **kwargs: Any) -> httpx.Response:
        started = monotonic()
        self.metrics.requests += 1
        try:
            response = await self.client.request(method.upper(), url, **kwargs)
            self.metrics.bytes_received += len(response.content)
            return response
        except Exception:
            self.metrics.failures += 1
            raise
        finally:
            self.metrics.total_duration_seconds += monotonic() - started

    async def get(self, url: str, **kwargs: Any) -> httpx.Response:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> httpx.Response:
        return await self.request("POST", url, **kwargs)

    async def aclose(self) -> None:
        await self.client.aclose()

    async def __aenter__(self) -> "ManagedAsyncClient":
        return self

    async def __aexit__(self, *_args: object) -> None:
        await self.aclose()
