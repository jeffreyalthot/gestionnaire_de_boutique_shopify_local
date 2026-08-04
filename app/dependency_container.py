from __future__ import annotations

import os
from dataclasses import dataclass
from time import monotonic
from typing import Any

import psutil

from ai.runtime.ai_runtime import AIRuntime
from analytics.collector import AnalyticsCollector
from app.automation_runtime import build_automation_supervisor
from app.command_bus import CommandBus
from app.event_bus import EventBus
from automation.exceptions.exception_classifier import ExceptionClassifier
from automation.core.autonomy_controller import AutonomyController
from automation.core.autonomy_kernel import ActionProposal, AutonomyKernel
from observability.health_registry import HealthRegistry
from app.mode_controller import ModeController
from app.query_bus import QueryBus
from app.recovery_manager import RecoveryManager
from app.runtime_coordinator import RuntimeCoordinator
from app.service_registry import ServiceRegistry
from automation.exceptions.exception_queue import ExceptionQueue
from config.settings import Settings
from customers.customer_repository import CustomerRepository
from customers.privacy.consent_ledger import ConsentLedger
from customers.segments.segment_builder import SegmentBuilder
from dashboard.dashboard_state import DashboardState
from finance.accounting_engine import AccountingEngine
from finance.double_entry_ledger import DoubleEntryLedger
from infrastructure.database.engine import Database
from infrastructure.queue.durable_queue import DurableQueue
from integrations.alibaba.client import AlibabaClient
from integrations.alibaba.gateway import AlibabaGateway
from integrations.currency.converter import CurrencyConverter
from integrations.currency.static_rate_provider import StaticRateProvider
from integrations.shopify.client import ShopifyClient
from integrations.shopify.graphql_transport import ShopifyGraphQLTransport
from integrations.shopify.webhooks.handler_registry import ShopifyWebhookHandlerRegistry
from pricing.pricing_engine import PricingEngine
from inventory.inventory_allocation import InventoryAllocation
from inventory.inventory_snapshot_repository import InventorySnapshotRepository
from marketing.campaign_repository import CampaignRepository
from observability.metric_registry import MetricRegistry
from observability.sqlite_metrics_sink import SqliteMetricsSink
from orders.order_repository import OrderRepository
from orders.order_timeline import OrderTimeline
from pricing.price_snapshot_repository import PriceSnapshotRepository
from procurement.purchase_intent_repository import PurchaseIntentRepository
from risk.fraud.order_fraud_rules import OrderFraudRules
from risk.risk_registry import RiskRegistry
from risk.risk_context import RiskContext
from risk.risk_score import RiskScore
from sales_channels.channel_registry import ChannelRegistry
from sales_channels.google_merchant_adapter import GoogleMerchantAdapter
from sales_channels.meta_catalog_adapter import MetaCatalogAdapter
from sales_channels.pos_adapter import POSAdapter
from sales_channels.shop_app_adapter import ShopAppAdapter
from sales_channels.tiktok_shop_adapter import TikTokShopAdapter
from security.emergency_lockdown import EmergencyLockdown
from security.oauth_state_store import OAuthStateStore
from procurement.procurement_engine import ProcurementEngine
from security.encryption import EncryptionService
from security.field_encryption import FieldEncryption
from security.pii_vault import PIIVault


@dataclass(slots=True)
class Container:
    settings: Settings
    db: Database
    queue: DurableQueue
    shopify_transport: ShopifyGraphQLTransport
    shopify: ShopifyClient
    alibaba_gateway: AlibabaGateway
    alibaba: AlibabaClient
    currency: CurrencyConverter
    pricing: PricingEngine
    procurement: ProcurementEngine
    ledger: DoubleEntryLedger
    accounting: AccountingEngine
    pii_vault: PIIVault
    ai: AIRuntime
    dashboard: DashboardState
    automation: Any
    resource_governor: Any
    automation_state: Any
    capabilities: Any
    operation_registry: Any
    command_bus: CommandBus
    event_bus: EventBus
    query_bus: QueryBus
    mode_controller: ModeController
    service_registry: ServiceRegistry
    health: HealthRegistry
    exception_router: ExceptionClassifier
    exception_queue: ExceptionQueue
    recovery: RecoveryManager
    runtime_coordinator: RuntimeCoordinator | None
    analytics: AnalyticsCollector
    customers: CustomerRepository
    consents: ConsentLedger
    segments: SegmentBuilder
    order_repository: OrderRepository
    order_timeline: OrderTimeline
    inventory_positions: InventorySnapshotRepository
    inventory_allocation: InventoryAllocation
    price_history: PriceSnapshotRepository
    purchase_intents: PurchaseIntentRepository
    risk_registry: RiskRegistry
    lockdown: EmergencyLockdown
    oauth_states: OAuthStateStore
    metrics_registry: MetricRegistry
    metrics_sink: SqliteMetricsSink
    campaigns: CampaignRepository
    sales_channels: ChannelRegistry
    webhook_handlers: ShopifyWebhookHandlerRegistry
    autonomy_kernel: AutonomyKernel

    def dashboard_state(self) -> dict[str, object]:
        process = psutil.Process(os.getpid())
        resource = self.resource_governor.sample()
        return {
            "counts": self.db.counts(),
            "finance": self.db.financial_snapshot(),
            "runtime": {
                "uptime_seconds": self.dashboard.uptime_seconds(),
                "dry_run": self.settings.app_dry_run,
                "rss_mb": process.memory_info().rss / 1048576,
                "cpu_percent": process.cpu_percent(None),
                "profile": self.settings.runtime_profile,
                "resource": resource,
            },
            "api": {
                "database": self.db.health(),
                "shopify_ready": self.settings.live_shopify_ready,
                "alibaba_ready": self.settings.live_alibaba_ready,
                "payment_ready": self.settings.live_payment_ready,
            },
            "ai": self.ai.status(),
            "queue": self.queue.stats(),
            "audit": self.db.verify_audit_chain(),
            "automation": self.automation_state.snapshot(),
            "capabilities": self.capabilities.snapshot(),
            "mode": self.mode_controller.snapshot(),
            "control_plane": {
                "services": len(self.service_registry.descriptors()),
                "queries": self.query_bus.snapshot(),
                "commands": self.command_bus.names(),
                "exceptions": self.exception_queue.stats(),
                "last_snapshot": self.runtime_coordinator.last_snapshot() if self.runtime_coordinator else None,
            },
            "privacy": {
                "profiles": int(self.db.scalar("SELECT COUNT(*) FROM customer_profiles", default=0)),
                "consents": int(self.db.scalar("SELECT COUNT(*) FROM customer_consents", default=0)),
                "segments": int(self.db.scalar("SELECT COUNT(*) FROM customer_segment_memberships", default=0)),
            },
            "commerce_control": {
                "purchase_intents": int(self.db.scalar("SELECT COUNT(*) FROM purchase_intents", default=0)),
                "purchase_intents_pending": int(self.db.scalar("SELECT COUNT(*) FROM purchase_intents WHERE status IN ('planned','approved','retry')", default=0)),
                "reserved_units": int(self.db.scalar("SELECT COALESCE(SUM(reserved),0) FROM inventory_positions", default=0)),
                "low_stock_positions": int(self.db.scalar("SELECT COUNT(*) FROM inventory_positions WHERE on_hand-reserved<=safety_stock", default=0)),
                "risk_holds": int(self.db.scalar("SELECT COUNT(*) FROM risk_decisions WHERE held=1", default=0)),
                "lockdown": self.lockdown.snapshot(),
                "metrics": self.metrics_registry.snapshot().values,
            },
            "integration_runtime": {
                "webhook_handlers": self.webhook_handlers.snapshot(),
                "sales_channels": self.sales_channels.snapshot(),
                "queue_by_channel": self.queue.stats_by_queue(),
                "shopify_transport": self.shopify_transport.stats().as_dict(),
                "alibaba_gateway": self.alibaba_gateway.stats().as_dict(),
            },
            "autonomy_kernel": self.autonomy_kernel.snapshot(),
            "native_plans": {
                str(row["status"]): int(row["count"])
                for row in self.db.query("SELECT status,COUNT(*) count FROM native_plans GROUP BY status")
            },
        }

    def status(self) -> dict[str, object]:
        return self.dashboard_state()

    async def close(self) -> None:
        await self.shopify_transport.close()
        await self.alibaba_gateway.close()


def build_container(settings: Settings) -> Container:
    db = Database(settings.database_path)
    db.initialize()
    queue = DurableQueue(db)
    shopify_transport = ShopifyGraphQLTransport(settings)
    shopify = ShopifyClient(shopify_transport)
    alibaba_gateway = AlibabaGateway(settings)
    alibaba = AlibabaClient(alibaba_gateway)
    currency = CurrencyConverter(StaticRateProvider())
    pricing = PricingEngine(settings)
    ledger = DoubleEntryLedger(db)
    accounting = AccountingEngine(ledger)
    encryption = EncryptionService(settings.master_encryption_key.get_secret_value())
    vault = PIIVault(FieldEncryption(encryption))
    procurement = ProcurementEngine(settings, db, alibaba)
    ai = AIRuntime(settings, db)
    automation, governor, state, capabilities, registry = build_automation_supervisor(settings, queue, db)

    command_bus = CommandBus()
    event_bus = EventBus()
    query_bus = QueryBus()
    services = ServiceRegistry()
    health = HealthRegistry()
    exception_router = ExceptionClassifier()
    exception_queue = ExceptionQueue(db)
    recovery = RecoveryManager(db, queue)
    analytics = AnalyticsCollector(db)
    customers = CustomerRepository(db)
    consents = ConsentLedger(db)
    segments = SegmentBuilder(db)
    order_repository = OrderRepository(db)
    order_timeline = OrderTimeline(db)
    inventory_positions = InventorySnapshotRepository(db)
    inventory_allocation = InventoryAllocation(db)
    price_history = PriceSnapshotRepository(db)
    purchase_intents = PurchaseIntentRepository(db)
    risk_registry = RiskRegistry()
    fraud_rules = OrderFraudRules()
    risk_registry.register("order_fraud", lambda context: fraud_rules.assess(context.attributes))
    lockdown = EmergencyLockdown()
    oauth_states = OAuthStateStore(db)
    metrics_registry = MetricRegistry()
    metrics_sink = SqliteMetricsSink(db)
    campaigns = CampaignRepository()
    sales_channels = ChannelRegistry()
    webhook_handlers = ShopifyWebhookHandlerRegistry()
    webhook_handlers.load_defaults()
    autonomy_kernel = AutonomyKernel(
        capabilities=capabilities,
        governor=governor,
        lockdown=lockdown,
        controller=AutonomyController(
            dry_run=settings.app_dry_run,
            minimum_confidence=settings.ai_minimum_autonomous_confidence,
            financial_limit_cad=settings.automation_financial_limit_cad,
        ),
        db=db,
    )
    sales_channels.register("google_merchant", GoogleMerchantAdapter())
    sales_channels.register("meta_catalog", MetaCatalogAdapter())
    sales_channels.register("tiktok_shop", TikTokShopAdapter())
    sales_channels.register("shop_app", ShopAppAdapter())
    sales_channels.register("pos", POSAdapter())

    container = Container(
        settings=settings,
        db=db,
        queue=queue,
        shopify_transport=shopify_transport,
        shopify=shopify,
        alibaba_gateway=alibaba_gateway,
        alibaba=alibaba,
        currency=currency,
        pricing=pricing,
        procurement=procurement,
        ledger=ledger,
        accounting=accounting,
        pii_vault=vault,
        ai=ai,
        dashboard=DashboardState(monotonic()),
        automation=automation,
        resource_governor=governor,
        automation_state=state,
        capabilities=capabilities,
        operation_registry=registry,
        command_bus=command_bus,
        event_bus=event_bus,
        query_bus=query_bus,
        mode_controller=ModeController(settings.app_dry_run),
        service_registry=services,
        health=health,
        exception_router=exception_router,
        exception_queue=exception_queue,
        recovery=recovery,
        runtime_coordinator=None,
        analytics=analytics,
        customers=customers,
        consents=consents,
        segments=segments,
        order_repository=order_repository,
        order_timeline=order_timeline,
        inventory_positions=inventory_positions,
        inventory_allocation=inventory_allocation,
        price_history=price_history,
        purchase_intents=purchase_intents,
        risk_registry=risk_registry,
        lockdown=lockdown,
        oauth_states=oauth_states,
        metrics_registry=metrics_registry,
        metrics_sink=metrics_sink,
        campaigns=campaigns,
        sales_channels=sales_channels,
        webhook_handlers=webhook_handlers,
        autonomy_kernel=autonomy_kernel,
    )

    for name, instance, critical, tags in (
        ("database", db, True, ("storage", "sqlite")),
        ("queue", queue, True, ("runtime", "durable")),
        ("shopify", shopify, False, ("integration", "commerce")),
        ("alibaba", alibaba, False, ("integration", "supplier")),
        ("automation", automation, True, ("runtime", "orchestration")),
        ("analytics", analytics, False, ("analytics",)),
        ("customers", customers, False, ("privacy", "customer")),
        ("orders", order_repository, True, ("commerce", "orders")),
        ("inventory", inventory_positions, True, ("commerce", "inventory")),
        ("pricing_history", price_history, False, ("commerce", "pricing")),
        ("purchase_intents", purchase_intents, True, ("commerce", "procurement")),
        ("risk", risk_registry, True, ("security", "risk")),
        ("lockdown", lockdown, True, ("security", "runtime")),
        ("metrics", metrics_registry, False, ("observability",)),
        ("campaigns", campaigns, False, ("marketing",)),
        ("sales_channels", sales_channels, False, ("commerce", "channels")),
        ("webhook_handlers", webhook_handlers, True, ("integration", "webhooks")),
        ("autonomy_kernel", autonomy_kernel, True, ("automation", "safety", "policy")),
    ):
        services.register(name, instance, critical=critical, tags=tags)

    health.register("database", db.health, critical=True)
    health.register("audit_chain", db.verify_audit_chain, critical=True)
    health.register("resource_budget", lambda: {
        "ok": bool(governor.sample()["within_memory_budget"]), **governor.sample()
    }, critical=True)
    health.register("queue", lambda: {
        "ok": int(queue.stats().get("dead", 0)) == 0,
        **queue.stats(),
    })
    health.register("emergency_lockdown", lambda: {
        "ok": not lockdown.snapshot()["active"],
        **lockdown.snapshot(),
    }, critical=True)
    health.register("autonomy_kernel", lambda: {
        "ok": not lockdown.snapshot()["active"],
        **autonomy_kernel.snapshot(),
    }, critical=True)
    health.register("shopify_configuration", lambda: {
        "ok": bool(settings.app_dry_run or settings.live_shopify_ready),
        "ready": settings.live_shopify_ready,
        "dry_run": settings.app_dry_run,
    })
    health.register("alibaba_configuration", lambda: {
        "ok": bool(settings.app_dry_run or settings.live_alibaba_ready),
        "ready": settings.live_alibaba_ready,
        "dry_run": settings.app_dry_run,
    })

    coordinator = RuntimeCoordinator(container, health, recovery)
    container.runtime_coordinator = coordinator
    services.register("runtime_coordinator", coordinator, critical=True, tags=("runtime", "health"))

    query_bus.register("runtime.status", lambda _: container.status())
    query_bus.register("runtime.services", lambda _: services.snapshot())
    query_bus.register("runtime.exceptions", lambda payload: exception_queue.claim_ready(int(payload.get("limit", 50))))
    query_bus.register("catalog.counts", lambda _: {
        "products": int(db.scalar("SELECT COUNT(*) FROM products", default=0)),
        "media": int(db.scalar("SELECT COUNT(*) FROM media_assets", default=0)),
        "suppliers": int(db.scalar("SELECT COUNT(*) FROM supplier_scores", default=0)),
    })
    query_bus.register("automation.autonomy", lambda _: autonomy_kernel.snapshot())
    query_bus.register("commerce.exposure", lambda _: {
        "purchase_intents": int(db.scalar("SELECT COUNT(*) FROM purchase_intents", default=0)),
        "reserved_units": int(db.scalar("SELECT COALESCE(SUM(reserved),0) FROM inventory_positions", default=0)),
        "risk_holds": int(db.scalar("SELECT COUNT(*) FROM risk_decisions WHERE held=1", default=0)),
        "active_campaigns": len(campaigns.list("active")),
    })

    async def command_snapshot(payload: dict[str, Any]) -> dict[str, Any]:
        snapshot = await coordinator.snapshot(persist=bool(payload.get("persist", True)))
        return snapshot.as_dict()

    async def command_recover(_: dict[str, Any]) -> dict[str, Any]:
        return coordinator.recover()

    async def command_cycle(_: dict[str, Any]) -> dict[str, Any]:
        return await automation.run_cycle()

    command_bus.register("runtime.snapshot", command_snapshot)
    command_bus.register("runtime.recover", command_recover)
    command_bus.register("automation.cycle", command_cycle)
    return container
