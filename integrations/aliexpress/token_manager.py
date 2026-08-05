"""AliExpress token manager for OAuth token create/refresh/revoke.

This module implements a pragmatic manager that calls the AliExpress OAuth
endpoints defined in settings and updates the in-memory Settings instance
with the new access/refresh tokens. It uses retries and an existing
backoff function for retriable HTTP errors.
"""

from __future__ import annotations

import asyncio
from time import monotonic
from typing import Any

import httpx
from pydantic import SecretStr

from config.settings import Settings, get_settings
from infrastructure.http.backoff import exponential_backoff
from integrations.alibaba.rate_limit_manager import AlibabaRateLimitManager
from observability.metrics import metrics


class AliExpressTokenManager:
    def __init__(self, settings: Settings | None = None, client: httpx.AsyncClient | None = None) -> None:
        self.settings = settings or get_settings()
        self.client = client or httpx.AsyncClient(timeout=self.settings.aliexpress_request_timeout_seconds)
        self._owns_client = client is None
        # Re-use the simple rate limit manager with configured rps
        self.rate_limit = AlibabaRateLimitManager(requests_per_second=float(self.settings.aliexpress_rate_limit_rps), burst=1)

    async def close(self) -> None:
        if self._owns_client:
            await self.client.aclose()

    async def _post(self, url: str, data: dict[str, Any]) -> dict[str, Any]:
        last: Exception | None = None
        started = monotonic()
        try:
            for attempt in range(self.settings.aliexpress_max_retries + 1):
                try:
                    waited = await self.rate_limit.wait()
                    if waited:
                        metrics.inc("aliexpress.token_rate_limit_wait_seconds", waited)

                    headers = {"Accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
                    response = await self.client.post(url, data=data, headers=headers)
                    metrics.inc("aliexpress.token_requests")
                    if response.status_code == 429 or response.status_code >= 500:
                        raise httpx.HTTPStatusError("Erreur AliExpress token récupérable", request=response.request, response=response)
                    response.raise_for_status()
                    payload = response.json()
                    if not isinstance(payload, dict):
                        raise ValueError("Réponse AliExpress token invalide")
                    return payload
                except (httpx.HTTPError, ValueError, RuntimeError) as exc:
                    last = exc
                    metrics.inc("aliexpress.token_errors")
                    if attempt >= self.settings.aliexpress_max_retries:
                        break
                    await asyncio.sleep(exponential_backoff(attempt))
            assert last is not None
            raise last
        finally:
            metrics.inc("aliexpress.token_request_duration_seconds", monotonic() - started)

    async def create_token_with_code(self, code: str, redirect_uri: str | None = None) -> dict[str, Any]:
        """Exchange an authorization code for tokens using POST /token/create.

        Returns the token payload as returned by AliExpress and also updates
        the in-memory settings (aliexpress_access_token / aliexpress_refresh_token) if present.
        """
        url = self.settings.aliexpress_oauth_token_url
        data: dict[str, Any] = {
            "grant_type": "authorization_code",
            "client_id": self.settings.aliexpress_app_key,
            "client_secret": self.settings.aliexpress_app_secret.get_secret_value() or "",
            "code": code,
        }
        if redirect_uri:
            data["redirect_uri"] = redirect_uri
        payload = await self._post(url, data)
        # Typical fields: access_token, refresh_token, expires_in
        if "access_token" in payload:
            setattr(self.settings, "aliexpress_access_token", SecretStr(str(payload.get("access_token") or "")))
        if "refresh_token" in payload:
            setattr(self.settings, "aliexpress_refresh_token", SecretStr(str(payload.get("refresh_token") or "")))
        return payload

    async def refresh_token(self, refresh_token: str | None = None) -> dict[str, Any]:
        """Refresh an access token using POST /token/refresh.

        If refresh_token is omitted, this function will try to use the value
        from settings.aliexpress_refresh_token.
        """
        token = refresh_token or (self.settings.aliexpress_refresh_token.get_secret_value() if self.settings.aliexpress_refresh_token else None)
        if not token:
            raise RuntimeError("Aucun refresh_token disponible pour AliExpress.")
        url = self.settings.aliexpress_oauth_refresh_url
        data: dict[str, Any] = {
            "grant_type": "refresh_token",
            "client_id": self.settings.aliexpress_app_key,
            "client_secret": self.settings.aliexpress_app_secret.get_secret_value() or "",
            "refresh_token": token,
        }
        payload = await self._post(url, data)
        if "access_token" in payload:
            setattr(self.settings, "aliexpress_access_token", SecretStr(str(payload.get("access_token") or "")))
        if "refresh_token" in payload:
            setattr(self.settings, "aliexpress_refresh_token", SecretStr(str(payload.get("refresh_token") or "")))
        return payload

    async def revoke_token(self, token: str | None = None) -> dict[str, Any]:
        """Revoke a token using POST /token/revoke.

        If token is omitted, the current access token from settings will be used.
        The method returns the provider response (often empty object on success).
        """
        t = token or (self.settings.aliexpress_access_token.get_secret_value() if self.settings.aliexpress_access_token else None)
        if not t:
            raise RuntimeError("Aucun token disponible pour révocation.")
        url = self.settings.aliexpress_oauth_refresh_url.rstrip("/") + "/revoke"
        data = {
            "client_id": self.settings.aliexpress_app_key,
            "client_secret": self.settings.aliexpress_app_secret.get_secret_value() or "",
            "token": t,
        }
        payload = await self._post(url, data)
        # Clear local settings values on success
        setattr(self.settings, "aliexpress_access_token", SecretStr(""))
        setattr(self.settings, "aliexpress_refresh_token", SecretStr(""))
        return payload
