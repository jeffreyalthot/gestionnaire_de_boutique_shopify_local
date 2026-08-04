from __future__ import annotations

from app.version import VERSION

import asyncio
from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any

import httpx

from config.settings import Settings
from infrastructure.http.backoff import exponential_backoff
from integrations.shopify.cost_calculator import query_cost
from integrations.shopify.deprecation_monitor import DeprecationMonitor
from integrations.shopify.error_mapper import ShopifyAPIError, raise_for_graphql_errors
from integrations.shopify.throttle_manager import ShopifyThrottleManager
from observability.metrics import metrics


@dataclass(frozen=True, slots=True)
class ShopifyTransportStats:
    requests: int
    retries: int
    errors: int
    total_seconds: float
    last_operation: str
    last_request_id: str
    last_cost: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ShopifyGraphQLTransport:
    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self.settings = settings
        self.client = client or httpx.AsyncClient(timeout=settings.shopify_request_timeout_seconds)
        self._owns_client = client is None
        self.throttle = ShopifyThrottleManager()
        self.deprecations = DeprecationMonitor()
        self.requests = self.retries = self.errors = 0
        self.total_seconds = 0.0
        self.last_operation = ""
        self.last_request_id = ""
        self.last_cost: dict[str, object] = {}
        self.last_extensions: dict[str, object] = {}

    async def close(self) -> None:
        if self._owns_client:
            await self.client.aclose()

    async def execute(self, query: str, variables: dict[str, Any] | None = None,
                      operation_name: str | None = None, estimated_cost: int = 10) -> dict[str, Any]:
        if not self.settings.live_shopify_ready:
            raise ShopifyAPIError("Configuration Shopify incomplète.")
        if not str(query).strip():
            raise ValueError("GraphQL query is required")
        headers = {
            "X-Shopify-Access-Token": self.settings.shopify_admin_access_token.get_secret_value(),
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"Shopify-Alibaba-AI-Orchestrator/{VERSION}",
        }
        body: dict[str, Any] = {"query": query, "variables": variables or {}}
        if operation_name:
            body["operationName"] = operation_name
        last: Exception | None = None
        started = monotonic()
        self.last_operation = operation_name or self._operation_from_query(query)
        try:
            for attempt in range(self.settings.shopify_max_retries + 1):
                try:
                    waited = await self.throttle.before_request(max(1, int(estimated_cost)))
                    if waited:
                        metrics.inc("shopify.throttle_wait_seconds", waited)
                    response = await self.client.post(self.settings.shopify_graphql_url, headers=headers, json=body)
                    self.requests += 1
                    metrics.inc("shopify.requests")
                    self.last_request_id = str(response.headers.get("X-Request-ID", response.headers.get("x-request-id", "")))
                    self.deprecations.inspect(response.headers, operation=self.last_operation)
                    if response.status_code == 429 or response.status_code >= 500:
                        raise httpx.HTTPStatusError("Erreur Shopify récupérable", request=response.request, response=response)
                    response.raise_for_status()
                    payload = response.json()
                    if not isinstance(payload, dict):
                        raise ShopifyAPIError("Réponse GraphQL Shopify invalide.")
                    raise_for_graphql_errors(payload)
                    self.last_extensions = dict(payload.get("extensions", {}) or {})
                    self.last_cost = query_cost(payload).as_dict()
                    await self.throttle.observe(payload.get("extensions"))
                    data = payload.get("data", {})
                    if data is None:
                        return {}
                    if not isinstance(data, dict):
                        raise ShopifyAPIError("Le champ data GraphQL doit être un objet.")
                    return data
                except (httpx.HTTPError, ShopifyAPIError, ValueError) as exc:
                    last = exc
                    self.errors += 1
                    metrics.inc("shopify.errors")
                    if attempt >= self.settings.shopify_max_retries:
                        break
                    self.retries += 1
                    await asyncio.sleep(exponential_backoff(attempt))
            assert last is not None
            raise last
        finally:
            self.total_seconds += monotonic() - started

    def stats(self) -> ShopifyTransportStats:
        return ShopifyTransportStats(
            self.requests, self.retries, self.errors, round(self.total_seconds, 6),
            self.last_operation, self.last_request_id, dict(self.last_cost),
        )

    @staticmethod
    def _operation_from_query(query: str) -> str:
        compact = " ".join(str(query).split())
        for marker in ("query ", "mutation "):
            if marker in compact:
                return compact.split(marker, 1)[1].split("(", 1)[0].split("{", 1)[0].strip()
        return "anonymous"
