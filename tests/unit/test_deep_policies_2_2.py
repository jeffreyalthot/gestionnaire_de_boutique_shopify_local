from __future__ import annotations
import pytest
from pydantic import ValidationError
from ai.policies.confidence_policy import evaluate_confidence
from ai.policies.human_approval_policy import approval_requirement
from ai.policies.safe_action_policy import SafeActionPolicy
from api.schemas.approvals import ApprovalDecision
from api.schemas.shipping import ShippingRate
from compliance.country_restriction_filter import evaluate_country
from compliance.tax_compliance import evaluate_tax_registration
from inventory.out_of_stock_handler import evaluate_stock_status
from inventory.safety_stock import calculate_safety_stock, inventory_decision
from marketing.email.replenishment_flow import ReplenishmentFlow
from marketing.email.winback_flow import WinbackFlow
from marketing.seo.keyword_map import KeywordMap
from marketing.seo.structured_data_builder import StructuredDataBuilder

def test_confidence_and_approval_are_risk_aware():
    assert evaluate_confidence(.95, .9).allowed
    assert not evaluate_confidence(.95, .9, risk_score=.5).allowed
    assert approval_requirement("refund", 1, 100).required
    assert approval_requirement("tag_product", 1, 100).required is False

def test_safe_action_policy_blocks_families():
    policy = SafeActionPolicy()
    assert policy.evaluate("update_inventory").safe
    assert not policy.evaluate("bypass_payment_confirmation").safe
    assert not policy.evaluate("disable_security_hmac").safe

def test_api_schemas_are_strict():
    assert ShippingRate(service_name="Standard", service_code="STD", total_price="12.50", currency="cad").currency == "CAD"
    with pytest.raises(ValidationError): ApprovalDecision(approved=False, actor="operator")
    with pytest.raises(ValidationError): ShippingRate(service_name="", service_code="X", total_price=-1, currency="CAD")

def test_country_and_tax_compliance_decisions():
    assert evaluate_country("ca", {"US"}).allowed
    assert not evaluate_country("US", {"us"}).allowed
    with pytest.raises(ValueError): evaluate_country("Canada", set())
    assert evaluate_tax_registration(30000).required
    assert evaluate_tax_registration(25000).remaining_before_threshold_cad == 5000

def test_inventory_dynamic_safety_and_stock_status():
    assert calculate_safety_stock(average_daily_sales=4, lead_time_days=10, variability_factor=.25) == 10
    decision = inventory_decision(20, 4, 3, average_daily_sales=2, lead_time_days=7, target_cover_days=20)
    assert decision.available == 13
    assert decision.reorder_point == 18
    assert evaluate_stock_status(0, continue_selling=True, supplier_available=True).publishable

def test_marketing_flows_require_consent_and_are_deterministic():
    assert ReplenishmentFlow().evaluate(90, 100).due
    assert not ReplenishmentFlow().evaluate(90, 100, marketing_consent=False).due
    assert WinbackFlow().evaluate(150, True, lifetime_orders=8).segment == "vip_lapsed"
    mapping = KeywordMap().assign(["a", "b"], ["One", "Two", "One", "Three"])
    assert mapping == {"a": ("one", "three"), "b": ("two",)}

def test_structured_data_is_complete():
    data = StructuredDataBuilder().product({"title":"Produit", "sku":"SKU-1", "price_cad":"12.5", "stock":3, "brand":"ELIT21"})
    assert data["offers"]["price"] == "12.50"
    assert data["brand"]["name"] == "ELIT21"
