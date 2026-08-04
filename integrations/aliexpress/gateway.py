"""AliExpress integration package - lightweight initial implementation.

This module provides a gateway to call AliExpress Open Platform REST endpoints
and a small client with a few commonly-used methods (products, orders, tracking).

Notes:
- OAuth/token endpoints and exact parameters may need to be adjusted to match
  the credentials and app settings you have on AliExpress Open Platform.
- This is intentionally a small, incremental implementation to let you switch
  to AliExpress while keeping the existing Alibaba code in place.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, asdict
from time import monotonic
from typing import Any

import httpx

from config.settings import Settings
from observability.metrics import metrics
from infrastructure.http.backoff import exponential_backoff


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
        self.client = client or httpx.AsyncClient(timeout=settings.aliexpress_request_timeout_seconds)
        self._owns_client = client is None
        self.requests = self.retries = self.errors = 0
        self.total_seconds = 0.0
        self.last_path = ""
        self.last_request_id = ""
        # simple in-memory rate limiter (tokens per second)
        self._rate_limit_rps = float(self.settings.aliexpress_rate_limit_rps)
        self._last_request_at = 0.0

    async def close(self) -> None:
        if self._owns_client:
            await self.client.aclose()

    async def _ensure_rate_limit(self) -> float:
        """Wait if necessary to respect a simple RPS limit. Returns seconds waited."""
        now = monotonic()
        min_interval = 1.0 / max(1.0, self._rate_limit_rps)
        waited = 0.0
        if now - self._last_request_at < min_interval:
            waited = min_interval - (now - self._last_request_at)
            await asyncio.sleep(waited)
        self._last_request_at = monotonic()
        return waited

    async def _attempt_token_refresh(self) -> None:
        """Attempt to refresh the AliExpress access token using refresh token.
        This is a best-effort flow; adjust to the exact AliExpress token API.
        """
        if not self.settings.aliexpress_refresh_token.get_secret_value():
            return
        url = self.settings.aliexpress_oauth_refresh_url
        data = {
            "grant_type": "refresh_token",
            "client_id": self.settings.aliexpress_app_key,
            "client_secret": self.settings.aliexpress_app_secret.get_secret_value(),
            "refresh_token": self.settings.aliexpress_refresh_token.get_secret_value(),
        }
        try:
            resp = await self.client.post(url, data=data, timeout=self.settings.aliexpress_request_timeout_seconds)
            if resp.status_code == 200:
                payload = resp.json()
                # payload structure depends on AliExpress response; common keys: access_token, refresh_token
                at = payload.get("access_token")
                rt = payload.get("refresh_token")
                if at:
                    # Note: Settings is frozen after startup in many deployments; here we only advise
                    # that caller persist the new token in their secret store / env if desired.
                    # For local dry-run this may be acceptable to set attribute directly.
                    try:
                        self.settings.aliexpress_access_token = type(self.settings.aliexpress_access_token)(at)
                    except Exception:
                        pass
                if rt:
                    try:
                        self.settings.aliexpress_refresh_token = type(self.settings.aliexpress_refresh_token)(rt)
                    except Exception:
                        pass
        except Exception:
            # token refresh is best-effort; swallow errors and let caller handle auth failures
            return

    async def call(self, path: str, method: str = "GET", params: dict[str, Any] | None = None,
                   json_body: dict[str, Any] | None = None, files: dict[str, Any] | None = None,
                   auth_required: bool = True) -> dict[str, Any]:
        if auth_required and not self.settings.live_aliexpress_ready:
            raise RuntimeError("Configuration AliExpress incomplète.")
        path = str(path).lstrip("/")
        url = f"{self.settings.aliexpress_base_url.rstrip('/')}/{path}"
        started = monotonic()
        last: Exception | None = None
        self.last_path = path
        for attempt in range(self.settings.aliexpress_max_retries + 1):
            try:
                waited = await self._ensure_rate_limit()
                if waited:
                    metrics.inc("aliexpress.rate_limit_wait_seconds", waited)
                headers = {"Accept": "application/json"}
                if auth_required:
                    headers["Authorization"] = f"Bearer {self.settings.aliexpress_access_token.get_secret_value()}"
                if files:
                    resp = await self.client.post(url, params=params, data=json_body or {}, files=files, headers=headers)
                elif method.upper() == "GET":
                    resp = await self.client.get(url, params=params, headers=headers)
                elif method.upper() == "POST":
                    resp = await self.client.post(url, json=json_body, params=params, headers=headers)
                else:
                    resp = await self.client.request(method.upper(), url, params=params, json=json_body, headers=headers)
                self.requests += 1
                metrics.inc("aliexpress.requests")
                self.last_request_id = str(resp.headers.get("x-request-id", ""))
                if resp.status_code == 401:
                    # try token refresh once
                    await self._attempt_token_refresh()
                    # if last attempt, break and raise
                    if attempt >= self.settings.aliexpress_max_retries:
                        resp.raise_for_status()
                    else:
                        self.retries += 1
                        await asyncio.sleep(exponential_backoff(attempt))
                        continue
                if resp.status_code >= 500 or resp.status_code == 429:
                    raise httpx.HTTPStatusError("AliExpress recoverable error", request=resp.request, response=resp)
                resp.raise_for_status()
                payload = resp.json()
                if not isinstance(payload, dict):
                    # wrap non-dict responses
                    return {"data": payload}
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

    def stats(self) -> AliExpressGatewayStats:
        # simple snapshot; rate_limit info minimal
        return AliExpressGatewayStats(
            self.requests, self.retries, self.errors, round(self.total_seconds, 6),
            self.last_path, self.last_request_id, {"rps": self._rate_limit_rps},
        )
