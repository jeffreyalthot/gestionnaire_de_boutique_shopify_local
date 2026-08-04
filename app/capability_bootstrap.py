from __future__ import annotations

from typing import Any


def capability_report(settings: Any) -> dict[str, dict[str, bool | str]]:
    return {
        "shopify.read": {"available": True, "mode": "simulated" if not settings.live_shopify_ready else "live"},
        "shopify.write": {"available": bool(settings.app_dry_run or settings.live_shopify_ready), "mode": "simulated" if settings.app_dry_run else "live"},
        "alibaba.read": {"available": bool(settings.app_dry_run or settings.live_alibaba_ready), "mode": "simulated" if settings.app_dry_run else "live"},
        "alibaba.write": {"available": bool(settings.app_dry_run or settings.live_alibaba_ready), "mode": "simulated" if settings.app_dry_run else "live"},
        "supplier.payment": {"available": bool(settings.app_dry_run or settings.live_payment_ready), "mode": "manual_gate" if not settings.live_payment_ready else "authorized_api"},
    }
