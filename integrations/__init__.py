"""Integration factory and convenience exports for supplier clients.

Provide a single factory function `get_supplier_client` that returns an
AlibabaClient-compatible object. If AliExpress is configured and ready,
it returns an adapter backed by AliExpress; otherwise it returns the
existing AlibabaClient.
"""

from __future__ import annotations

from typing import Any

from config.settings import get_settings
from integrations.alibaba.client import AlibabaClient
from integrations.alibaba.gateway import AlibabaGateway

try:
    from integrations.aliexpress.gateway import AliExpressGateway
    from integrations.aliexpress.client import AliExpressClient
    from integrations.aliexpress.adapter import AliExpressAdapter
except Exception:  # pragma: no cover - optional dependency in repo
    AliExpressGateway = AliExpressClient = AliExpressAdapter = None  # type: ignore


def get_supplier_client(settings=None) -> Any:
    settings = settings or get_settings()
    # Prefer AliExpress when configured
    if getattr(settings, "live_aliexpress_ready", False) and AliExpressGateway is not None:
        gateway = AliExpressGateway(settings)
        client = AliExpressClient(gateway)
        return AliExpressAdapter(client)
    # Fallback to Alibaba
    gateway = AlibabaGateway(settings)
    return AlibabaClient(gateway)
