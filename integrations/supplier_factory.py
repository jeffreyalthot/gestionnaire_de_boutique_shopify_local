"""Factory to obtain supplier client for the configured provider.

Usage:
    from integrations import get_supplier_client
    client = get_supplier_client()

The factory prefers the SUPPLIER_PROVIDER env (via Settings) and falls back
on the Alibaba client when AliExpress is not configured.
"""
from __future__ import annotations

import os
from typing import Optional

from config.settings import get_settings

# Lazy imports to avoid import cycles / heavy modules at import time


def get_supplier_client(provider: Optional[str] = None, **kwargs):
    settings = get_settings()
    provider = (provider or os.getenv("SUPPLIER_PROVIDER") or "alibaba").lower()
    if provider == "aliexpress":
        try:
            from integrations.aliexpress.client import AliExpressClient
            from integrations.aliexpress.gateway import AliExpressGateway

            gateway = kwargs.pop("gateway", None) or AliExpressGateway(settings)
            return AliExpressClient(gateway=gateway)
        except Exception:
            # Fall back to Alibaba when AliExpress is not available
            provider = "alibaba"

    # Default: Alibaba
    from integrations.alibaba.client import AlibabaClient
    from integrations.alibaba.gateway import AlibabaGateway

    gateway = kwargs.pop("gateway", None) or AlibabaGateway(get_settings())
    return AlibabaClient(gateway=gateway)
