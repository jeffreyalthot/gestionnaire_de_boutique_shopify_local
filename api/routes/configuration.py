from __future__ import annotations

from fastapi import APIRouter


def router_for(container):
    router = APIRouter(tags=["configuration"])

    @router.get("/configuration/capabilities")
    async def capabilities():
        settings = container.settings
        return {
            "dry_run": settings.app_dry_run,
            "runtime_profile": settings.runtime_profile,
            "shopify_ready": settings.live_shopify_ready,
            "alibaba_ready": settings.live_alibaba_ready,
            "payment_ready": settings.live_payment_ready,
            "payment_card_storage": False,
            "api_mutations_enabled": settings.api_mutations_enabled,
            "capabilities": container.capabilities.snapshot(),
            "services": container.service_registry.snapshot(),
        }

    return router
