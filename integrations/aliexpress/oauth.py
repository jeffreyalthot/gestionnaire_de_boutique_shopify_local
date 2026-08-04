"""Minimal OAuth helpers for AliExpress Open Platform.

These helpers do not persist tokens themselves — they return the token data for
the caller to store (for example via a TokenManager). The functions are
intended to be used during initial app authorization and for manual token
exchange in a console or admin flow.
"""
from __future__ import annotations

from typing import Dict, Any

import httpx

from config.settings import get_settings


async def create_token_with_code(code: str) -> Dict[str, Any]:
    settings = get_settings()
    async with httpx.AsyncClient(timeout=settings.aliexpress_request_timeout_seconds) as client:
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.aliexpress_app_key,
            "client_secret": settings.aliexpress_app_secret.get_secret_value(),
            "code": code,
            "redirect_uri": settings.alibaba_callback_url or "",
        }
        response = await client.post(settings.aliexpress_oauth_token_url, data=data)
        response.raise_for_status()
        return response.json()


async def refresh_token(refresh_token: str) -> Dict[str, Any]:
    settings = get_settings()
    async with httpx.AsyncClient(timeout=settings.aliexpress_request_timeout_seconds) as client:
        data = {
            "grant_type": "refresh_token",
            "client_id": settings.aliexpress_app_key,
            "client_secret": settings.aliexpress_app_secret.get_secret_value(),
            "refresh_token": refresh_token,
        }
        response = await client.post(settings.aliexpress_oauth_refresh_url, data=data)
        response.raise_for_status()
        return response.json()
