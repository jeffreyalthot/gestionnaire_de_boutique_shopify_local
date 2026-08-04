from __future__ import annotations

from automation.core.automation_state import AutomationState
from automation.core.automation_supervisor import AutomationSupervisor
from automation.core.capability_matrix import CapabilityMatrix
from automation.core.operation_registry import OperationDefinition, OperationRegistry
from automation.core.runtime_budget import ResourceGovernor, RuntimeBudget


def build_operation_registry(settings) -> OperationRegistry:
    registry = OperationRegistry()
    definitions = [
        OperationDefinition("shopify_webhook_drain", "shopify.read", "webhooks", 10, False, "read_only", 10),
        OperationDefinition("paid_order_intake", "shopify.read", "orders", 15, False, "read_only", 30),
        OperationDefinition("order_risk_review", "shopify.read", "orders", 20, False, "read_only", 30),
        OperationDefinition("supplier_order_planning", "alibaba.order", "procurement", 25, False, "reversible", 30),
        OperationDefinition("supplier_payment_review", "alibaba.payment", "payments", 30, False, "financial", 60),
        OperationDefinition("tracking_reconciliation", "alibaba.read", "fulfillment", 35, False, "read_only", settings.tracking_sync_interval_seconds),
        OperationDefinition("shopify_fulfillment_sync", "shopify.write", "fulfillment", 40, False, "reversible", 60),
        OperationDefinition("inventory_reconciliation", "shopify.write", "inventory", 45, False, "reversible", settings.inventory_sync_interval_seconds),
        OperationDefinition("supplier_stock_recheck", "alibaba.read", "inventory", 50, False, "read_only", 120),
        OperationDefinition("price_recalculation", "shopify.write", "pricing", 55, False, "reversible", settings.price_sync_interval_seconds),
        OperationDefinition("catalog_discovery", "alibaba.read", "catalog", 60, True, "read_only", settings.product_discovery_interval_seconds),
        OperationDefinition("catalog_quality_review", "alibaba.read", "catalog", 65, False, "read_only", 300),
        OperationDefinition("media_import", "media.import", "media", 70, True, "reversible", 300),
        OperationDefinition("catalog_publication_review", "shopify.write", "catalog", 75, False, "irreversible", 300),
        OperationDefinition("customer_ticket_triage", "customer.reply", "customer_service", 80, False, "read_only", 30),
        OperationDefinition("return_refund_review", "shopify.write", "returns", 85, False, "financial", 60),
        OperationDefinition("financial_reconciliation", "finance.reconcile", "finance", 90, False, "read_only", 300),
        OperationDefinition("payout_reconciliation", "shopify.read", "finance", 95, False, "read_only", 3600),
        OperationDefinition("compliance_rescan", "alibaba.read", "compliance", 100, True, "read_only", 3600),
        OperationDefinition("runtime_health_snapshot", "runtime.local", "maintenance", 5, False, "read_only", 60),
        OperationDefinition("exception_recovery", "runtime.local", "maintenance", 8, False, "reversible", 60),
        OperationDefinition("database_maintenance", "finance.reconcile", "maintenance", 110, False, "reversible", 3600),
        OperationDefinition("analytics_snapshot", "analytics.local", "maintenance", 115, False, "read_only", 300),
        OperationDefinition("catalog_lifecycle_review", "analytics.local", "catalog", 118, False, "read_only", 1800),
        OperationDefinition("supplier_score_refresh", "analytics.local", "catalog", 120, False, "read_only", 1800),
        OperationDefinition("customer_profile_refresh", "privacy.local", "customer_service", 125, False, "reversible", 3600),
        OperationDefinition("privacy_retention_review", "privacy.local", "compliance", 130, False, "read_only", 21600),
        OperationDefinition("marketing_budget_review", "finance.reconcile", "finance", 135, False, "read_only", 3600),
        OperationDefinition("financial_reserve_review", "finance.reconcile", "finance", 140, False, "read_only", 3600),
        OperationDefinition("inventory_reservation_audit", "analytics.local", "inventory", 142, False, "read_only", 300),
        OperationDefinition("purchase_intent_recovery", "runtime.local", "procurement", 145, False, "reversible", 120),
        OperationDefinition("fraud_posture_snapshot", "analytics.local", "orders", 148, False, "read_only", 300),
        OperationDefinition("campaign_schedule_review", "analytics.local", "marketing", 150, False, "read_only", 900),
        OperationDefinition("store_configuration_audit", "shopify.read", "maintenance", 152, False, "read_only", 3600),
        OperationDefinition("sales_channel_review", "shopify.read", "catalog", 154, False, "read_only", 1800),
        OperationDefinition("security_integrity_review", "runtime.local", "maintenance", 156, False, "read_only", 300),
        OperationDefinition("oauth_state_cleanup", "runtime.local", "maintenance", 158, False, "reversible", 600),
        OperationDefinition("dead_letter_review", "runtime.local", "maintenance", 160, False, "read_only", 300),
        OperationDefinition("channel_feed_review", "analytics.local", "catalog", 162, False, "read_only", 900),
        OperationDefinition("tax_reserve_review", "finance.reconcile", "finance", 164, False, "read_only", 1800),
        OperationDefinition("consent_expiry_review", "privacy.local", "compliance", 166, False, "read_only", 3600),
    ]
    for definition in definitions:
        registry.register(definition)
    return registry


def build_automation_supervisor(settings, queue, db):
    budget = RuntimeBudget(
        max_rss_mb=float(settings.runtime_max_rss_mb),
        max_cpu_percent=float(settings.runtime_max_cpu_percent),
        max_http_concurrency=int(settings.max_concurrent_http_requests),
        max_heavy_operations_per_cycle=int(settings.runtime_max_heavy_operations_per_cycle),
        max_pending_tasks=int(settings.runtime_max_pending_tasks),
        max_media_cache_mb=int(settings.runtime_media_cache_mb),
        worker_threads=2,
    )
    governor = ResourceGovernor(budget)
    state = AutomationState()
    capabilities = CapabilityMatrix.from_settings(settings)
    registry = build_operation_registry(settings)
    supervisor = AutomationSupervisor(registry=registry, capabilities=capabilities, governor=governor, state=state, queue=queue, db=db, dry_run=settings.app_dry_run)
    return supervisor, governor, state, capabilities, registry
