from __future__ import annotations

import asyncio
import random
import ssl
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from customer_service.ticket_router import TicketRouter
from fulfillment.address_validator import AddressValidator, validate_shipping_address
from fulfillment.customs_data_builder import CustomsDataBuilder, build_customs_line
from fulfillment.late_shipment_detector import LateShipmentDetector, is_late
from infrastructure.http.backoff import BackoffPolicy
from infrastructure.http.connection_pool import ConnectionLimiter
from infrastructure.http.tls import secure_ssl_context
from infrastructure.queue.delayed_queue import DelayedQueue
from infrastructure.queue.durable_queue import DurableQueue
from infrastructure.queue.priority_queue import PriorityQueue
from localization.locale_registry import LocaleRegistry
from localization.store_translation import StoreTranslation
from localization.translation_memory import TranslationMemory
from observability.action_trace import ActionTrace
from observability.alert_manager import AlertManager
from observability.metric_registry import MetricRegistry
from pricing.discount_margin_guard import DiscountMarginGuard
from pricing.dynamic_margin_policy import DynamicMarginPolicy
from pricing.markup_calculator import MarkupCalculator, sale_price_for_markup
from pricing.platform_fee_estimator import PlatformFeeEstimator
from pricing.price_guardrails import PriceGuardrails, validate_price
from pricing.shipping_subsidy_policy import ShippingSubsidyPolicy
from pricing.tax_estimator import TaxEstimator
from quality.completeness_checker import CompletenessChecker
from quality.data_quality_score import DataQualityScore
from reports.csv_exporter import export_csv
from reports.json_exporter import export_json
from returns.refund_policy import RefundPolicy
from returns.restocking_service import RestockingService
from returns.return_request import ReturnRequest
from returns.return_validator import ReturnValidator
from risk.fraud.order_fraud_rules import OrderFraudRules
from security.access_control import AccessControl, verify_admin_token
from security.data_retention import DataRetentionPolicy
from security.request_signing import RequestSigner
from supplier_intelligence.supplier_candidate import SupplierCandidate
from supplier_intelligence.supplier_capacity import SupplierCapacity
from supplier_intelligence.supplier_discovery import SupplierDiscovery
from supplier_intelligence.supplier_ranker import SupplierRanker
from supplier_intelligence.supplier_score import SupplierScore
from tax.province_rule_registry import ProvinceRuleRegistry
from tax.tax_category_mapper import TaxCategoryMapper
from tax.tax_reconciliation import TaxReconciliation
from workers.specialized_worker import SpecializedWorker


def test_address_validator_normalizes_canadian_address():
    result = AddressValidator().validate({"firstName":" A ","lastName":"B","address1":" 1 rue ","city":"Montréal","countryCodeV2":"ca","zip":"h2x 1y4","provinceCode":"QC"})
    assert result.valid and result.normalized["countryCodeV2"] == "CA"
    assert result.normalized["zip"] == "H2X 1Y4"


def test_address_validator_reports_missing_and_postal_errors():
    errors = validate_shipping_address({"countryCodeV2":"CA","zip":"bad"})
    assert "Code postal invalide pour le pays" in errors
    assert any("firstName" in error for error in errors)


def test_customs_builder_validates_and_totals():
    builder = CustomsDataBuilder()
    manifest = builder.manifest([{"description":"Widget","quantity":2,"value":"12.50","hs_code":"123456","origin":"ca","weight_kg":"0.2"}])
    assert manifest["total_value"] == "25.00"
    assert build_customs_line("Widget",1,5,"123456","CA")["countryCodeOfOrigin"] == "CA"


def test_customs_builder_rejects_invalid_hs():
    with pytest.raises(ValueError): CustomsDataBuilder().build_line("x",1,1,"12345","CA")


def test_late_detector_has_action_and_severity():
    old = datetime.now(timezone.utc) - timedelta(days=12)
    result = LateShipmentDetector().assess(old, 5)
    assert result.late and result.severity == "high" and result.next_action == "open_claim"
    assert is_late(old.isoformat(), 5)


def test_refund_policy_requires_return_for_change_of_mind():
    decision = RefundPolicy().decide(paid_cad=100,requested_cad=50,reason="changed_mind",delivered=True,days_since_delivery=5)
    assert not decision.approved and decision.reason == "return_required"


def test_refund_policy_caps_balance_and_flags_chargeback():
    decision = RefundPolicy().decide(paid_cad=100,requested_cad=90,refunded_cad=40,reason="chargeback",delivered=False,days_since_delivery=0)
    assert decision.amount_cad == 60 and decision.approval_required and "financial_dispute" in decision.risk_flags


def test_restocking_assessment_quarantines_unsafe_items():
    result = RestockingService().assess(received=10,damaged=2,missing=1,unsafe=2,unit_cost_cad=4)
    assert result.restockable == 5 and result.quarantine == 2 and result.inventory_value_cad == Decimal("20")


def test_return_validator_detects_duplicates_and_quantity():
    request = ReturnRequest("r","o","damaged",({"sku":"A","quantity":1},{"sku":"A","quantity":0}))
    result = ReturnValidator().assess(request)
    assert not result.valid and "invalid_item_quantity" in result.issues and "duplicate_item" in result.warnings


def test_ticket_router_escalates_high_value():
    route = TicketRouter().plan("refund", amount_cad=800)
    assert route.team == "returns" and route.priority == "high" and route.sla_minutes == 60


def test_dynamic_margin_explains_adjustments():
    result = DynamicMarginPolicy().evaluate(base_margin_percent=30, return_risk=.5, competition=.2, supplier_risk=.5)
    assert result.target_percent > 30 and result.adjustments["supplier_risk"] > 0


def test_price_guardrails_detect_large_change_warning():
    result = PriceGuardrails().evaluate(30, 10, 20, reference_price=10, maximum_change_percent=50)
    assert result.allowed and "large_price_change" in result.warnings
    validate_price(Decimal("30"),Decimal("10"),Decimal("20"))


def test_price_guardrails_rejects_low_margin():
    with pytest.raises(ValueError): validate_price(Decimal("10"),Decimal("9"),Decimal("20"))


def test_discount_guard_caps_and_checks_floor():
    result = DiscountMarginGuard().plan(regular_price_cad=100,discount_percent=90,landed_cost_cad=20,maximum_discount_percent=50)
    assert result.applied_percent == 50 and "discount_capped" in result.reasons


def test_fraud_rules_return_explainable_score():
    score = OrderFraudRules().assess({"proxy_or_vpn":True,"total_amount":1200,"account_age_days":0,"customer_chargebacks":1})
    assert score.score > .5 and score.factors and score.recommended_action in {"hold","block"}


def test_risk_score_trust_history_reduces_score():
    risky = OrderFraudRules().assess({"billing_shipping_mismatch":True,"total_amount":100})
    trusted = OrderFraudRules().assess({"billing_shipping_mismatch":True,"total_amount":100,"customer_order_count":10})
    assert trusted.score < risky.score


def test_backoff_policy_is_bounded_and_retry_after_wins():
    policy = BackoffPolicy(base_seconds=1,maximum_seconds=5,jitter_ratio=0)
    assert policy.delay(10,rng=random.Random(1)) == 5
    assert policy.delay(1,retry_after=3) == 3


def test_connection_limiter_collects_stats():
    async def run():
        limiter = ConnectionLimiter(1)
        async with limiter.slot(): pass
        return limiter.stats()
    stats = asyncio.run(run())
    assert stats.acquired_total == 1 and stats.active == 0


def test_secure_tls_context_requires_verification():
    context = secure_ssl_context()
    assert context.minimum_version >= ssl.TLSVersion.TLSv1_2 and context.verify_mode == ssl.CERT_REQUIRED


def test_delayed_and_priority_queues(db):
    queue = DurableQueue(db)
    delayed = DelayedQueue(queue).enqueue("sync",{},"delay-key",5)
    urgent = PriorityQueue(queue).enqueue("urgent",{},"urgent-key",priority="critical")
    assert delayed.delay_seconds == 5 and urgent.priority == 20
    rows = db.query("SELECT id,priority FROM tasks ORDER BY priority")
    assert {row["id"] for row in rows} == {delayed.task_id, urgent.task_id}


def test_access_control_and_token_verification():
    control = AccessControl()
    assert control.authorize("u",["operator"],"queue:retry").allowed
    assert not control.authorize("u",["viewer"],"queue:retry").allowed
    assert verify_admin_token("abc","abc") and not verify_admin_token("abc","")


def test_request_signer_prevents_replay_and_expiry():
    signer = RequestSigner("secret",tolerance_seconds=60)
    signed = signer.sign(b"body",timestamp=100,nonce="n")
    assert signer.verify(b"body",signed,now=100)
    assert not signer.verify(b"body",signed,now=100)
    expired = signer.sign(b"body",timestamp=0,nonce="x")
    assert not signer.verify(b"body",expired,now=100)


def test_data_retention_respects_legal_hold():
    policy = DataRetentionPolicy({"temporary":7})
    old = datetime.now(timezone.utc)-timedelta(days=10)
    assert policy.evaluate("temporary",old).delete_eligible
    assert not policy.evaluate("temporary",old,legal_hold=True).delete_eligible


def test_locale_registry_language_fallback():
    registry = LocaleRegistry(("fr-CA","en-CA"),"fr-CA")
    assert registry.resolve("en-US") == "en-CA"
    assert registry.resolve_details("es-MX").fallback_used


def test_translation_memory_persists(tmp_path):
    path = tmp_path/"translations.db"
    TranslationMemory(path).put("Hello","en-CA","fr-CA","Bonjour",quality=.9)
    memory = TranslationMemory(path)
    assert memory.get("Hello","en-CA","fr-CA") == "Bonjour"
    result = StoreTranslation(memory).resolve_details("Unknown","en-CA","fr-CA")
    assert result.missing and result.text == "Unknown"


def test_markup_and_fee_calculations_are_decimal_safe():
    result = MarkupCalculator().calculate("10","50")
    assert result.price == Decimal("15.00") and sale_price_for_markup(Decimal("10"),Decimal("50")) == Decimal("15.00")
    fee = PlatformFeeEstimator().estimate("100","2.9","0.30")
    assert fee.total_fee == Decimal("3.20") and fee.net_amount == Decimal("96.80")


def test_shipping_subsidy_is_capped_by_profit():
    result = ShippingSubsidyPolicy().evaluate(order_value_cad=100,gross_profit_cad=20,requested_cad=10)
    assert result.approved_cad == 6 and not result.allowed


def test_tax_estimator_supports_inclusive_tax():
    result = TaxEstimator().estimate("114.98","14.975",inclusive=True)
    assert result.total == Decimal("114.98") and result.tax > 0


def test_completeness_checker_validates_fields():
    result = CompletenessChecker().assess({"title":"x","price":-1},("title","price"),validators={"price":lambda value: value>0})
    assert not result.complete and "price" in result.invalid


def test_data_quality_score_has_grade_and_warnings():
    result = DataQualityScore().evaluate({"title":1,"images":.2},{"title":1,"images":2})
    assert result.grade in {"D","F"} and "low:images" in result.warnings


def test_supplier_capacity_detailed_assessment():
    result = SupplierCapacity().assess(monthly_capacity=100,committed=40,requested=30,buffer_percent=10)
    assert result.supported and result.remaining_after_order == 20


def test_supplier_discovery_filters_unverified():
    candidates = [SupplierCandidate("a","A","CN",2,verified=True),SupplierCandidate("b","B","CN",.5,verified=False)]
    result = SupplierDiscovery().evaluate(candidates,minimum_years=1,require_verified=True)
    assert [item.supplier_id for item in result.accepted] == ["a"] and result.rejected[0][0] == "b"


def test_supplier_ranker_returns_gap_to_leader():
    scores={"a":SupplierScore.calculate(quality=1,delivery=1,communication=1,compliance=1,price=1),"b":SupplierScore.calculate(quality=.5,delivery=.5,communication=.5,compliance=.5,price=.5)}
    ranked=SupplierRanker().detailed(scores)
    assert ranked[0].selected and ranked[1].gap_to_leader > 0


def test_province_tax_registry_components():
    rule=ProvinceRuleRegistry().get("QC")
    assert rule.combined_rate == .14975 and len(rule.components)==2


def test_tax_category_and_reconciliation():
    assert TaxCategoryMapper().resolve("t-shirt").category == "clothing"
    result=TaxReconciliation().reconcile("15","14.97",tolerance_cad=".01")
    assert not result.matched and result.action in {"review_rounding","open_tax_exception"}


def test_metric_registry_histograms_and_prefix():
    metrics=MetricRegistry()
    metrics.increment("orders.total"); metrics.set("orders.open",2)
    for value in (1,2,3,4): metrics.observe("latency",value)
    snapshot=metrics.snapshot(prefix="orders")
    assert snapshot.get("orders.total")==1 and "latency.p95" not in snapshot.values
    assert metrics.snapshot().get("latency.p95")==4


def test_alert_manager_deduplicates_and_acknowledges():
    manager=AlertManager()
    first=manager.add("error","boom"); second=manager.add("error","boom")
    assert first.fingerprint==second.fingerprint and second.occurrences==2
    assert manager.acknowledge(first.fingerprint)
    assert manager.snapshot(include_acknowledged=False)==[]


def test_action_trace_context_and_child():
    with ActionTrace("parent") as trace:
        child=trace.child("child",order_id="1"); child.finish()
    assert trace.status=="ok" and trace.duration_ms is not None and child.parent_id==trace.trace_id


def test_report_exporters_are_atomic_and_csv_safe(tmp_path):
    csv_path=export_csv([{"name":"=SUM(A1:A2)","value":1}],tmp_path/"report.csv")
    json_path=export_json({"ok":True},tmp_path/"report.json")
    assert "'=SUM" in csv_path.read_text(encoding="utf-8-sig")
    assert '"ok": true' in json_path.read_text()


def test_specialized_worker_retries_and_records_result():
    attempts={"n":0}
    async def handler(payload):
        attempts["n"]+=1
        if attempts["n"]==1: raise RuntimeError("temporary")
        return payload["value"]*2
    class Demo(SpecializedWorker): accepted_task_types=("demo",)
    result=asyncio.run(Demo(handler,retries=1).run_once("demo",{"value":3}))
    assert result.status=="completed" and result.result==6 and result.attempts==2
