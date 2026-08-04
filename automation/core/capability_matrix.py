from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Capability:
    name: str
    configured: bool
    live_allowed: bool
    reason: str = ""


class CapabilityMatrix:
    def __init__(self, capabilities: list[Capability]) -> None:
        self._items = {item.name: item for item in capabilities}

    @classmethod
    def from_settings(cls, settings: Any) -> "CapabilityMatrix":
        dry = bool(settings.app_dry_run)
        return cls([
            Capability("shopify.read", settings.live_shopify_ready or dry, True),
            Capability("shopify.write", settings.live_shopify_ready or dry, not dry),
            Capability("alibaba.read", settings.live_alibaba_ready or dry, True),
            Capability("alibaba.order", settings.live_alibaba_ready or dry, not dry),
            Capability("alibaba.payment", settings.live_payment_ready or dry, not dry and not settings.alibaba_require_manual_payment_approval),
            Capability("media.import", settings.live_shopify_ready or dry, not dry),
            Capability("customer.reply", True, not dry),
            Capability("finance.reconcile", True, True),
            Capability("runtime.local", True, True),
            Capability("analytics.local", True, True),
            Capability("privacy.local", True, True),
        ])

    def allows(self, name: str, *, live: bool = False) -> bool:
        item = self._items.get(name)
        return bool(item and item.configured and (not live or item.live_allowed))

    def snapshot(self) -> dict[str, dict[str, Any]]:
        return {name: {"configured": item.configured, "live_allowed": item.live_allowed, "reason": item.reason} for name, item in self._items.items()}
