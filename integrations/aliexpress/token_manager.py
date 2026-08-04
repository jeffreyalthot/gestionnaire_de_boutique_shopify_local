"""Token manager for AliExpress.

This class offers a thin facade to create/refresh/revoke tokens. It deliberately
keeps persistence out of scope — the caller should persist tokens securely
(e.g. database or vault) and update Settings/environment accordingly.
"""
from __future__ import annotations

from typing import Any, Dict

from config.settings import get_settings
from integrations.aliexpress.oauth import create_token_with_code, refresh_token as refresh_token_call


class AliExpressTokenManager:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def create_token(self, code: str) -> Dict[str, Any]:
        return await create_token_with_code(code)

    async def refresh(self, refresh_token: str) -> Dict[str, Any]:
        return await refresh_token_call(refresh_token)

    async def revoke(self, refresh_token: str) -> None:
        # AliExpress may provide a revoke endpoint; if not, callers should delete tokens on their side.
        return None
