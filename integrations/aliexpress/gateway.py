"""AliExpress Open Platform client and gateway implementations.

These provide a minimal, high-level client surface used by the existing
AlibabaClient delegation logic. The goal is to expose methods with the same
semantic names that AlibabaClient expects (search_products, get_product,
get_product_inventory, create_order, list_orders, get_order, tracking, etc.)
but implemented against the AliExpress REST Open Platform (v2).

This implementation is intentionally small and pragmatic — it performs HTTP
requests to the AliExpress base URL configured in settings and returns
parsed JSON responses. It uses the existing exponential_backoff utility for
retries and reuses the Alibaba rate-limit manager for simplicity.
"""

from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any

import httpx

from config.settings import Settings
from infrastructure.http.backoff import exponential_backoff
from integrations.alibaba.rate_limit_manager import AlibabaRateLimitManager
from observability.metrics import metrics


@dataclass(frozen=True, slots=True)
class AliExpressGatewayStats:
    requests: int
    retries: int
    errors: int
    total_seconds: float
    last_path: str
    last_request_id: str
    rate_limit: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class AliExpressGateway:
    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self.settings = settings
        self.base_url = settings.aliexpress_base_url.rstrip("/")
        self.client = client or httpx.AsyncClient(timeout=settings.aliexpress_request_timeout_seconds)
        self._owns_client = client is None
        self.rate_limit = AlibabaRateLimitManager(requests_per_second=float(settings.aliexpress_rate_limit_rps), burst=2)
        self.requests = self.retries = self.errors = 0
        self.total_seconds = 0.0
        self.last_path = ""
        self.last_request_id = ""

    async def close(self) -> None:
        if self._owns_client:
            await self.client.aclose()

    async def request(self, path: str, method: str = "GET", params: dict[str, Any] | None = None,
                      json: Any | None = None, files: dict[str, tuple[str, bytes, str]] | None = None) -> dict[str, Any]:
        if not self.settings.live_aliexpress_ready:
            raise RuntimeError("Configuration AliExpress incomplète.")
        path = path if path.startswith("/") else f"/{path}"
        url = f"{self.base_url}{path}"
        headers = {
            "Accept": "application/json",
        }
        token = self.settings.aliexpress_access_token.get_secret_value()
        if token:
            headers["Authorization"] = f"Bearer {token}"

        last: Exception | None = None
        started = monotonic()
        self.last_path = path
        try:
            for attempt in range(self.settings.aliexpress_max_retries + 1):
                try:
                    waited = await self.rate_limit.wait()
                    if waited:
                        metrics.inc("aliexpress.rate_limit_wait_seconds", waited)
                    if method.upper() == "GET":
                        response = await self.client.get(url, params=params, headers=headers)
                    elif method.upper() == "POST":
                        # Support JSON body or multipart files
                        if files:
                            response = await self.client.post(url, data=params or {}, files=files, headers=headers)
                        else:
                            response = await self.client.post(url, json=json, params=params, headers=headers)
                    else:
                        response = await self.client.request(method.upper(), url, params=params, json=json, headers=headers)

                    self.requests += 1
                    metrics.inc("aliexpress.requests")
                    self.last_request_id = str(response.headers.get("x-request-id", ""))
                    if response.status_code == 429 or response.status_code >= 500:
                        raise httpx.HTTPStatusError("Erreur AliExpress récupérable", request=response.request, response=response)
                    response.raise_for_status()
                    payload = response.json()
                    if not isinstance(payload, dict):
                        raise ValueError("Réponse AliExpress invalide.")
                    # Basic error mapping could be added here; for now return payload
                    return payload
                except (httpx.HTTPError, ValueError, RuntimeError) as exc:
                    last = exc
                    self.errors += 1
                    metrics.inc("aliexpress.errors")
                    if attempt >= self.settings.aliexpress_max_retries:
                        break
                    self.retries += 1
                    await asyncio.sleep(exponential_backoff(attempt))
            assert last is not None
            raise last
        finally:
            self.total_seconds += monotonic() - started

    def stats(self) -> AliExpressGatewayStats:
        return AliExpressGatewayStats(
            self.requests, self.retries, self.errors, round(self.total_seconds, 6),
            self.last_path, self.last_request_id, self.rate_limit.snapshot().as_dict(),
        )
