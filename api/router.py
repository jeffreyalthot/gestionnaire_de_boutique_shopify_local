from __future__ import annotations

from fastapi import APIRouter

from api.routes.analytics import router_for as analytics_router
from api.routes.automation import router_for as automation_router
from api.routes.configuration import router_for as config_router
from api.routes.dashboard_data import router_for as dashboard_router
from api.routes.exceptions import router_for as exceptions_router
from api.routes.health import router_for as health_router
from api.routes.manual_approvals import router_for as approvals_router
from api.routes.metrics import router_for as metrics_router
from api.routes.status import router_for as status_router
from api.routes.runtime import router_for as runtime_router
from api.routes.queues import router_for as queues_router
from api.routes.reports import router_for as reports_router
from integrations.shopify.webhooks.deduplicator import WebhookDeduplicator
from integrations.shopify.webhooks.dispatcher import ShopifyWebhookDispatcher
from integrations.shopify.webhooks.receiver import build_shopify_webhook_router


def build_router(container) -> APIRouter:
    router = APIRouter(prefix="/api")
    router.include_router(health_router(container))
    router.include_router(metrics_router())
    router.include_router(status_router(container))
    router.include_router(runtime_router(container))
    router.include_router(queues_router(container))
    router.include_router(reports_router(container))
    router.include_router(config_router(container))
    router.include_router(dashboard_router(container))
    router.include_router(automation_router(container))
    router.include_router(exceptions_router(container))
    router.include_router(analytics_router(container))
    router.include_router(approvals_router(container.db, container.procurement.gate))
    hooks = build_shopify_webhook_router(
        container.settings,
        WebhookDeduplicator(container.db),
        ShopifyWebhookDispatcher(container.queue),
    )
    router.include_router(hooks)
    return router
