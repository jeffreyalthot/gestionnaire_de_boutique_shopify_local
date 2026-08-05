"""AliExpress OAuth helpers (URL builders, authorize URL)"""

from __future__ import annotations

from urllib.parse import urlencode
from config.settings import get_settings


def build_authorize_url(redirect_uri: str, state: str | None = None, scope: str | None = None) -> str:
    settings = get_settings()
    params = {
        "client_id": settings.aliexpress_app_key,
        "response_type": "code",
        "redirect_uri": redirect_uri,
    }
    if state:
        params["state"] = state
    if scope:
        params["scope"] = scope
    base = settings.aliexpress_oauth_authorize_url.rstrip("/")
    return f"{base}?{urlencode(params)}"
