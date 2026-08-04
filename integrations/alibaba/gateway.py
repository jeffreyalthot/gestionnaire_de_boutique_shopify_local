from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any

import httpx

from config.settings import Settings
from infrastructure.http.backoff import exponential_backoff
from integrations.alibaba.error_mapper import inspect_alibaba_response
from integrations.alibaba.rate_limit_manager import AlibabaRateLimitManager
from integrations.alibaba.request_builder import encode_business_parameters
from integrations.alibaba.response_parser import parse_response
from integrations.alibaba.signer import AlibabaSigner
from integrations.alibaba.timestamp_service import alibaba_timestamp
from observability.metrics import metrics


@dataclass(frozen=True, slots=True)
class AlibabaGatewayStats:
    requests: int
    retries: int
    errors: int
    total_seconds: float
    last_method: str
    last_request_id: str
    rate_limit: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class AlibabaGateway:
    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None) -> None:
        self.settings = settings
        self.client = client or httpx.AsyncClient(timeout=settings.alibaba_request_timeout_seconds)
        self._owns_client = client is None
        self.signer = AlibabaSigner(
            settings.alibaba_app_secret.get_secret_value() or "dry-run-secret",
            settings.alibaba_sign_method,
        )
        self.rate_limit = AlibabaRateLimitManager(requests_per_second=2, burst=2)
        self.requests = self.retries = self.errors = 0
        self.total_seconds = 0.0
        self.last_method = ""
        self.last_request_id = ""

    async def close(self) -> None:
        if self._owns_client:
            await self.client.aclose()

    async def call(self, method: str, business_params: dict[str, Any] | None = None,
                   session_required: bool = True,
                   files: dict[str, tuple[str, bytes, str]] | None = None) -> dict[str, Any]:
        if not self.settings.live_alibaba_ready:
            raise RuntimeError("Configuration Alibaba incomplète.")
        method = str(method).strip()
        if not method:
            raise ValueError("Alibaba method is required")
        common: dict[str, Any] = {
            "method": method,
            "app_key": self.settings.alibaba_app_key,
            "timestamp": alibaba_timestamp(),
            "format": "json",
            "v": "2.0",
            "sign_method": self.settings.alibaba_sign_method,
        }
        if session_required:
            common["session"] = self.settings.alibaba_access_token.get_secret_value()
        params = {**common, **encode_business_parameters(business_params or {})}
        signed = self.signer.signed_params(params)
        last: Exception | None = None
        started = monotonic()
        self.last_method = method
        try:
            for attempt in range(self.settings.alibaba_max_retries + 1):
                try:
                    waited = await self.rate_limit.wait()
                    if waited:
                        metrics.inc("alibaba.rate_limit_wait_seconds", waited)
                    if files:
                        response = await self.client.post(self.settings.alibaba_gateway_url, data=signed, files=files)
                    else:
                        response = await self.client.post(self.settings.alibaba_gateway_url, data=signed)
                    self.requests += 1
                    metrics.inc("alibaba.requests")
                    self.last_request_id = str(response.headers.get("x-request-id", ""))
                    if response.status_code == 429 or response.status_code >= 500:
                        raise httpx.HTTPStatusError("Erreur Alibaba récupérable", request=response.request, response=response)
                    response.raise_for_status()
                    payload = response.json()
                    if not isinstance(payload, dict):
                        raise ValueError("Réponse Alibaba invalide.")
                    inspect_alibaba_response(payload)
                    parsed = parse_response(payload)
                    self.last_request_id = parsed.request_id or self.last_request_id
                    return payload
                except (httpx.HTTPError, ValueError, RuntimeError) as exc:
                    last = exc
                    self.errors += 1
                    metrics.inc("alibaba.errors")
                    if attempt >= self.settings.alibaba_max_retries:
                        break
                    self.retries += 1
                    await asyncio.sleep(exponential_backoff(attempt))
            assert last is not None
            raise last
        finally:
            self.total_seconds += monotonic() - started

    def stats(self) -> AlibabaGatewayStats:
        return AlibabaGatewayStats(
            self.requests, self.retries, self.errors, round(self.total_seconds, 6),
            self.last_method, self.last_request_id, self.rate_limit.snapshot().as_dict(),
        )
