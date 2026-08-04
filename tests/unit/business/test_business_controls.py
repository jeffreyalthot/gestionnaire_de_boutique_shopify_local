from datetime import datetime, timedelta, timezone

from analytics.forecasting import moving_average_forecast
from analytics.kpi_registry import default_registry
from customer_service.refund_request_classifier import RefundRequestClassifier
from customer_service.response_template_engine import ResponseTemplateEngine
from customer_service.ticket_priority import calculate_priority
from marketing.discount_guardrails import DiscountGuardrails
from orders.order_risk_assessor import OrderRiskAssessor
from orders.order_router import route_order
from orders.oversell_guard import allocate
from quality.quality_gate import QualityGate
from returns.refund_calculator import RefundCalculator
from returns.return_eligibility import ReturnEligibility
from risk.anomaly_rules import detect_anomalies
from risk.financial_exposure import FinancialExposureGuard
from risk.velocity_guard import VelocityGuard
from suppliers.due_diligence import DueDiligence
from suppliers.offer_comparator import compare_offers
from suppliers.supplier_score import SupplierScorer


def test_supplier_score_and_due_diligence():
    score = SupplierScorer().score("s1", {"on_time": .95, "quality": .9, "response": .9, "trade_assurance": 1, "years": .8, "refund_resolution": .9, "inventory_accuracy": .9})
    assert score.risk_level == "low"
    assert DueDiligence().evaluate({"verified_business": True, "years_active": 3, "dispute_rate": .01, "trade_assurance": True}).accepted


def test_offer_comparison_respects_moq():
    ranked = compare_offers([
        {"id": "cheap", "unit_cost": 1, "shipping_cost": 1, "delivery_days": 20, "supplier_score": .8, "moq": 100},
        {"id": "eligible", "unit_cost": 2, "shipping_cost": 1, "delivery_days": 10, "supplier_score": .9, "moq": 1},
    ], quantity=2)
    assert ranked[0]["id"] == "eligible"


def test_order_risk_and_routing():
    risk = OrderRiskAssessor().assess({"amount": 1000, "billing_shipping_mismatch": True, "orders_last_hour": 5})
    assert risk.hold
    assert route_order({"financial_status": "paid", "risk_level": "high"}) == "manual_risk_review"


def test_oversell_guard():
    assert allocate(10, 5, safety_stock=2, already_reserved=1).allowed
    assert not allocate(10, 8, safety_stock=2, already_reserved=1).allowed


def test_velocity_and_exposure_guards():
    velocity = VelocityGuard(limit=2)
    assert velocity.register("customer")
    assert velocity.register("customer")
    assert not velocity.register("customer")
    exposure = FinancialExposureGuard(100)
    assert exposure.evaluate(50, 40).allowed
    assert not exposure.evaluate(50, 60).allowed


def test_robust_anomaly_detection():
    assert detect_anomalies([10, 11, 10, 9, 10, 200]) == [5]


def test_customer_service_tools():
    assert RefundRequestClassifier().classify("The item is broken")[0] == "damaged_item"
    assert ResponseTemplateEngine().render("Hello {name}", {"name": "Jeff"}) == "Hello Jeff"
    assert calculate_priority("chargeback") < calculate_priority("other")


def test_return_and_refund_controls():
    now = datetime.now(timezone.utc)
    eligibility = ReturnEligibility().evaluate(delivered_at=now - timedelta(days=5), requested_at=now, category="general")
    assert eligibility.eligible
    refund = RefundCalculator().calculate(100, 15, 10, refund_shipping=True, restocking_percent=10)
    assert refund.total == 115


def test_discount_quality_analytics_and_forecast():
    assert not DiscountGuardrails().evaluate(100, 70, 30, 40).allowed
    assert QualityGate().evaluate({"media": .9, "supplier": .8}).passed
    kpis = default_registry().calculate({"orders": 10, "sessions": 100, "revenue": 500, "cogs": 250, "refunds": 1})
    assert kpis["conversion_rate"] == .1
    assert len(moving_average_forecast([1, 2, 3], horizon=4)) == 4
