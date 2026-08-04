"""Gateway for AliExpress Open Platform REST APIs.

This module implements a minimal, robust async gateway that sends requests to
https://api-sg.aliexpress.com/rest and performs common error handling,
rate limiting and metrics. It intentionally mirrors the behavior of the
Alibaba gateway so the rest of the application can easily switch providers.
"""
from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any, Dict, Optional

import httpx

from config.settings import Settings, get_settings
from integrations.alibaba.rate_limit_manager import AlibabaRateLimitManager
from integrations.aliexpress.error_mapper import inspect_aliexpress_response
from integrations.aliexpress.response_parser import parse_response
from observability.metrics import metrics


@dataclass(frozen=True, slots=True)
class AliExpressGatewayStats:
    requests: int
    retries: int
    errors: int
    total_seconds: float
    last_path: str
    last_request_id: str
    rate_limit: Dict[str, object]

    def as_dict(self) -> Dict[str, object]:
        return asdict(self)


class AliExpressGateway:
    def __init__(self, settings: Settings | None = None, client: httpx.AsyncClient | None = None) -> None:
        self.settings = settings or get_settings()
        self.client = client or httpx.AsyncClient(timeout=self.settings.aliexpress_request_timeout_seconds)
        self._owns_client = client is None
        # Rate limit manager reused from Alibaba integration because it is generic
        self.rate_limit = AlibabaRateLimitManager(requests_per_second=float(self.settings.aliexpress_rate_limit_rps), burst=2)
        self.requests = self.retries = self.errors = 0
        self.total_seconds = 0.0
        self.last_path = ""
        self.last_request_id = ""

    async def close(self) -> None:
        if self._owns_client:
            await self.client.aclose()

    async def call(self, path: str, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None,
                   method: str = "GET", session_required: bool = True,
                   files: Optional[Dict[str, tuple[str, bytes, str]]] = None) -> Dict[str, Any]:
        if not self.settings.live_aliexpress_ready:
            raise RuntimeError("Configuration AliExpress incomplète.")

        path = str(path)
        if not path.startswith("/"):
            path = "/" + path
        url = self.settings.aliexpress_base_url.rstrip("/") + path
        headers = {"accept": "application/json"}
        if session_required:
            token = self.settings.aliexpress_access_token.get_secret_value() or ""
            if token:
                headers["Authorization"] = f"Bearer {token}"

        started = monotonic()
        last: Exception | None = None
        self.last_path = path
        try:
            for attempt in range(int(self.settings.aliexpress_max_retries) + 1):
                try:
                    waited = await self.rate_limit.wait()
                    if waited:
                        metrics.inc("aliexpress.rate_limit_wait_seconds", waited)
                    if files:
                        # httpx expects files in the form {field: (filename, bytes, content_type)}
                        response = await self.client.post(url, headers=headers, params=params or {}, files=files)
                    elif method.upper() == "GET":
                        response = await self.client.get(url, headers=headers, params=params or {})
                    else:
                        response = await self.client.request(method.upper(), url, headers=headers, params=params or {}, json=body)

                    self.requests += 1
                    metrics.inc("aliexpress.requests")
                    self.last_request_id = str(response.headers.get("x-request-id", ""))

                    # Retry on server errors / rate limit
                    if response.status_code == 429 or response.status_code >= 500:
                        raise httpx.HTTPStatusError("Erreur AliExpress récupérable", request=response.request, response=response)
                    response.raise_for_status()

                    payload = response.json()
                    if not isinstance(payload, dict):
                        raise ValueError("Réponse AliExpress invalide.")

                    inspect_aliexpress_response(payload)
                    parsed = parse_response(payload)
                    self.last_request_id = parsed.get("request_id") or self.last_request_id
                    return payload

                except (httpx.HTTPError, ValueError, RuntimeError) as exc:
                    last = exc
                    self.errors += 1
                    metrics.inc("aliexpress.errors")
                    if attempt >= int(self.settings.aliexpress_max_retries):
                        break
                    self.retries += 1
                    await asyncio.sleep(0.5 * (2 ** attempt))
            assert last is not None
            raise last
        finally:
            self.total_seconds += monotonic() - started

    def stats(self) -> AliExpressGatewayStats:
        return AliExpressGatewayStats(
            self.requests, self.retries, self.errors, round(self.total_seconds, 6),
            self.last_path, self.last_request_id, self.rate_limit.snapshot().as_dict(),
        )
