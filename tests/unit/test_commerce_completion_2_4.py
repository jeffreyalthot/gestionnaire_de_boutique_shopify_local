from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from fulfillment.customer_notification_planner import CustomerNotificationPlanner
from fulfillment.delivery_option_selector import DeliveryOptionSelector, select_option
from fulfillment.fulfillment_sync import FulfillmentSync
from fulfillment.shipping_quote_cache import ShippingQuoteCache
from infrastructure.database.engine import Database, utcnow
from procurement.cancellation_handler import CancellationHandler
from procurement.payment_capability_gate import PaymentCapabilityGate
from procurement.payment_idempotency import PaymentIdempotency
from procurement.payment_result_monitor import PaymentResultMonitor
from procurement.purchase_compensator import PurchaseCompensator
from procurement.stock_recheck_service import StockRecheckService
from procurement.supplier_message_builder import SupplierMessageBuilder
from procurement.supplier_order_monitor import SupplierOrderMonitor
from returns.chargeback_monitor import ChargebackMonitor
from returns.return_analytics import ReturnAnalytics
from returns.return_label_planner import ReturnLabelPlanner
from returns.return_repository import ReturnRepository
from returns.return_request import ReturnRequest
from returns.return_shipping_tracker import ReturnShippingTracker


def make_db(tmp_path: Path) -> Database:
    db = Database(tmp_path / "shop.db")
    db.initialize()
    return db


def insert_order(db: Database, order_id: str = "o1", status: str = "pending") -> None:
    db.execute(
        "INSERT INTO orders(id,shopify_order_id,name,currency,total_amount,financial_status,fulfillment_status,procurement_status,payload_json,created_at,updated_at) "
        "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
        (order_id, f"gid://shopify/Order/{order_id}", "#1001", "CAD", 100, "paid", "unfulfilled", status, "{}", utcnow(), utcnow()),
    )


def test_payment_capability_gate_explains_limits_and_simulation():
    gate = PaymentCapabilityGate(maximum_amount_cad=100)
    assert gate.decide(provider_ready=False, approved=False, dry_run=True, amount_cad=1000).allowed
    decision = gate.decide(provider_ready=True, approved=True, dry_run=False, amount_cad=150)
    assert not decision.allowed and decision.reason == "amount_limit_exceeded"
    assert gate.evaluate(provider_ready=True, approved=True, dry_run=False) == (True, "allowed")


def test_payment_idempotency_is_stable_and_tracks_completion():
    tracker = PaymentIdempotency(maximum_entries=10)
    first = tracker.begin(supplier_order_id="s1", amount="12.345", currency="cad")
    second = tracker.begin(supplier_order_id="s1", amount=12.35, currency="CAD")
    assert first.key == second.key and first.amount == "12.35"
    paid = tracker.complete(first.key, status="paid", external_reference="p1")
    assert paid.status == "paid" and paid.external_reference == "p1"


def test_payment_result_monitor_classifies_terminal_result():
    class Client:
        async def payment_result(self, order_id: str):
            return {"status": "paid", "payment_id": "p1", "order_id": order_id}

    result = asyncio.run(PaymentResultMonitor(Client()).inspect("s1"))
    assert result.terminal and result.successful and not result.retryable


def test_stock_recheck_supports_buffers_and_partial_availability():
    service = StockRecheckService()
    assert service.check(2, 2) == (True, "available")
    decision = service.decide(5, 4, safety_buffer=1, allow_partial=True)
    assert decision.allowed and decision.reason == "partial_available" and decision.shortage == 2


def test_supplier_message_builder_returns_structured_instructions():
    builder = SupplierMessageBuilder()
    message = builder.build(order_reference="A-1", fragile=True, custom_instructions=["Use blue box"])
    assert "A-1" in message and "fragile" in message.lower() and "blue box" in message.lower()
    assert len(builder.instructions(order_reference="A-1")) >= 4


def test_supplier_order_monitor_escalates_overdue_orders():
    monitor = SupplierOrderMonitor()
    assert monitor.action("paid", age_hours=73) == "contact_supplier"
    severe = monitor.assess("paid", age_hours=121)
    assert severe.overdue and severe.severity == "high" and severe.action == "escalate_supplier"


def test_purchase_compensator_orders_reversible_actions():
    plan = PurchaseCompensator().build_plan(
        intent_status="paid",
        supplier_supports_cancel=True,
        payment_captured=True,
    )
    assert plan[0].action == "cancel_supplier_order"
    assert {step.action for step in plan} >= {"request_supplier_refund", "release_inventory_reservation", "open_exception"}


def test_cancellation_handler_is_conditional_and_releases_reservations(tmp_path: Path):
    db = make_db(tmp_path)
    insert_order(db)
    db.execute(
        "INSERT INTO order_lines(id,order_id,shopify_line_id,sku,title,quantity,unit_revenue_cad) VALUES(?,?,?,?,?,?,?)",
        ("l1", "o1", "sl1", "SKU", "Item", 2, 50),
    )
    db.execute(
        "INSERT INTO inventory_positions(sku,location_id,on_hand,reserved,safety_stock,incoming,updated_at) VALUES(?,?,?,?,?,?,?)",
        ("SKU", "default", 10, 3, 0, 0, utcnow()),
    )
    result = CancellationHandler(db).cancel("o1", "customer_request")
    assert result.cancelled and result.status == "cancelled"
    assert db.scalar("SELECT reserved FROM inventory_positions WHERE sku='SKU'") == 1
    assert CancellationHandler(db).cancel("o1", "repeat").cancelled is False


def test_delivery_selector_applies_cost_speed_reliability_and_tracking():
    selector = DeliveryOptionSelector()
    options = [
        {"carrier": "cheap", "amount": 5, "estimated_days": 40, "tracking": True, "reliability": .8},
        {"carrier": "fast", "amount": 8, "estimated_days": 5, "tracking": True, "reliability": .95},
        {"carrier": "no-track", "amount": 1, "estimated_days": 2, "tracking": False},
    ]
    decision = selector.select(options, maximum_days=60, maximum_amount_cad=20, preferred_carriers=("fast",))
    assert decision.option["carrier"] == "fast" and decision.rejected_count == 1
    assert select_option(options)["carrier"] in {"cheap", "fast"}


def test_shipping_quote_cache_normalizes_postal_code_and_finds_cheapest():
    cache = ShippingQuoteCache(default_ttl_seconds=60)
    key1 = cache.key("p", "s", "ca", "H2X 1Y4", 1)
    key2 = cache.key("p", "s", "CA", "h2x1y4", 1)
    assert key1 == key2
    cache.store(key1, {"amount": 10})
    cache.store("other", {"amount": 5})
    assert cache.cheapest([key1, "other"])["amount"] == 5


def test_fulfillment_sync_detects_unchanged_tracking():
    class Tracking:
        async def sync(self, shipment):
            return {"status": "in_transit", "tracking_number": "T1"}

    sync = FulfillmentSync(Tracking())
    shipment = {"id": "sh1", "supplier_order_id": "s1"}
    first = asyncio.run(sync.synchronize(shipment))
    second = asyncio.run(sync.synchronize(shipment))
    assert first.changed and not second.changed and first.fingerprint == second.fingerprint


def test_notification_planner_generates_deduplication_key_and_priority():
    planner = CustomerNotificationPlanner()
    plan = planner.build_plan("in_transit", "lost", order_id="o1", tracking_number="T1", sms_available=True)
    assert plan.send and plan.priority == "high" and plan.deduplication_key.endswith(":T1")
    assert planner.plan("delivered", "delivered")["reason"] == "no_status_change"


def test_return_analytics_calculates_financial_and_preventable_rates():
    rows = [
        {"reason": "damaged", "refund_amount_cad": 20, "product_id": "p1", "supplier_id": "s1"},
        {"reason": "late_delivery", "refund_amount_cad": 10, "product_id": "p1", "supplier_id": "s1"},
    ]
    summary = ReturnAnalytics().detailed(rows, orders=10)
    assert summary.return_rate == .2 and summary.refund_amount_cad == 30
    assert summary.preventable_rate == 1 and "audit_supplier_and_product_quality" in summary.recommendations


def test_return_label_planner_handles_economic_and_hazardous_returns():
    planner = ReturnLabelPlanner()
    assert planner.plan(reason="damaged", item_value_cad=100, return_shipping_cad=10) == "merchant_paid_label"
    assert planner.detailed_plan(reason="changed_mind", item_value_cad=10, return_shipping_cad=8).return_required is False
    assert planner.detailed_plan(reason="damaged", item_value_cad=100, return_shipping_cad=10, hazardous=True).approval_required


def test_return_repository_validates_state_machine_and_history():
    repo = ReturnRepository()
    repo.save(ReturnRequest("r1", "o1", "damaged"))
    approved = repo.transition("r1", "approved", reason="eligible")
    assert approved.status == "approved" and len(repo.history("r1")) == 2
    with pytest.raises(ValueError):
        repo.transition("r1", "closed")
    assert repo.by_order("o1")[0].id == "r1"


def test_return_shipping_tracker_explains_overdue_actions():
    tracker = ReturnShippingTracker()
    assert tracker.action("label_created", 8) == "customer_reminder"
    assessment = tracker.assess("in_transit", 22)
    assert assessment.overdue and assessment.action == "escalate_carrier" and assessment.severity == "high"


def test_chargeback_monitor_calculates_reserve_and_checkpoint(tmp_path: Path):
    db = make_db(tmp_path)
    db.execute(
        "INSERT INTO payments(id,supplier_order_id,amount,currency,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
        ("p1", "s1", 500, "CAD", "chargeback", utcnow(), utcnow()),
    )
    db.execute(
        "INSERT INTO payments(id,supplier_order_id,amount,currency,status,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
        ("p2", "s2", 100, "CAD", "disputed", utcnow(), utcnow()),
    )
    result = ChargebackMonitor(db).run()
    assert result.cases == 2 and result.amount_cad == 600 and result.reserve_cad == 690
    assert db.get_value("returns:chargeback_monitor:last_run")

from app.resource_governor import ResourceGovernor, RuntimeBudget
from infrastructure.cache.sqlite_cache import SQLiteCache
from infrastructure.database.health_check import DatabaseHealthChecker, check_database
from infrastructure.http.proxy import parse_proxy
from infrastructure.scheduler.missed_job_recovery import MissedJobRecovery, record_run
from integrations.currency.rate_cache import ExchangeRateCache
from integrations.notifications.critical_alert_notifier import CriticalAlertNotifier
from localization.fallback_locale_policy import FallbackLocalePolicy
from localization.unit_presenter import UnitPresenter
from quality.order_quality_gate import OrderQualityGate
from risk.fraud.customer_fraud_history import CustomerFraudHistory


def test_application_resource_governor_issues_permits_and_stats():
    governor = ResourceGovernor(RuntimeBudget(max_rss_mb=10_000, max_cpu_percent=1000))
    governor.begin_cycle("c1")
    permit = governor.request(heavy=False)
    assert permit.allowed
    with governor.operation():
        pass
    assert governor.operational_stats()["operations_started"] == 2


def test_database_health_checker_reports_sqlite_details(tmp_path: Path):
    db = make_db(tmp_path)
    health = DatabaseHealthChecker(db).inspect()
    assert health.ok and health.integrity == "ok" and health.database_bytes > 0
    assert check_database(db)["detailed"]["ok"] is True


def test_proxy_parser_redacts_credentials_and_rejects_private_hosts():
    config = parse_proxy("https://user:secret@proxy.example.com:8443")
    assert config.authenticated and "secret" not in config.safe_for_logs
    with pytest.raises(ValueError):
        parse_proxy("http://127.0.0.1:8080")


def test_missed_job_recovery_detects_overdue_and_records_run(tmp_path: Path):
    db = make_db(tmp_path)
    now = datetime.now(timezone.utc)
    record_run(db, "sync", (now - timedelta(seconds=500)).isoformat())
    missed = MissedJobRecovery(db).inspect([("sync", 60), ("new", 60)], now=now)
    assert {job.name for job in missed} == {"sync", "new"}
    assert next(job for job in missed if job.name == "sync").action == "run_and_reconcile"


def test_exchange_rate_cache_converts_and_handles_identity():
    cache = ExchangeRateCache()
    cache.store_rate("USD", "CAD", "1.35", source="test")
    assert str(cache.convert("10", "USD", "CAD")) == "13.50"
    assert str(cache.get_rate("CAD", "CAD").rate) == "1"


def test_critical_alert_notifier_suppresses_repeated_noise():
    class Service:
        def __init__(self): self.messages=[]
        def critical(self, message): self.messages.append(message)
    service=Service(); notifier=CriticalAlertNotifier(service)
    first=notifier.send("database unavailable", repeat_every=3)
    second=notifier.send("database unavailable", repeat_every=3)
    third=notifier.send("database unavailable", repeat_every=3)
    assert first.delivered and second.suppressed and third.delivered and len(service.messages)==2


def test_locale_fallback_and_unit_presenter_are_french_canadian():
    policy=FallbackLocalePolicy()
    assert policy.chain("fr_CA")[:2] == ("fr-CA", "fr")
    assert policy.resolve("fr-FR", {"fr", "en"}) == "fr"
    presenter=UnitPresenter()
    assert presenter.weight(1250) == "1,25 kg"
    assert presenter.money("12.5") == "12,50 $ CA"


def test_order_quality_gate_separates_blocking_issues():
    decision=OrderQualityGate().decide({"id":"o1","total":10,"lines":[{"quantity":1}],"shipping_address":{"address1":"1 Main","city":"Montreal","country_code":"CA","postal_code":"H2X1Y4"}})
    assert decision.passed
    bad=OrderQualityGate().decide({"total":-1,"lines":[]})
    assert not bad.passed and bad.blocking_issues and bad.action=="reject_or_correct"


def test_customer_fraud_history_is_explainable():
    assessment=CustomerFraudHistory().assess(chargebacks=1,failed_payments=2,total_orders=2,account_age_days=2)
    assert assessment.hold and assessment.level in {"high","critical"}
    assert "chargeback_history" in assessment.reasons


def test_sqlite_cache_ttl_get_or_set_and_stats(tmp_path: Path):
    db=make_db(tmp_path); cache=SQLiteCache(db,"unit")
    cache.set("a",{"value":1},ttl_seconds=60)
    assert cache.get("a")["value"]==1
    assert cache.get_or_set("a",lambda:{"value":2})["value"]==1
    assert cache.delete("a") and cache.get("a") is None
    assert cache.stats()=={"hits":2,"misses":1}
