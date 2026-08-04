from __future__ import annotations

from datetime import datetime, timezone

from quality.catalog_quality_gate import CatalogQualityGate
from returns.refund_policy import RefundPolicy
from returns.return_label_planner import ReturnLabelPlanner
from returns.return_request import ReturnRequest
from returns.return_validator import ReturnValidator
from supplier_intelligence.due_diligence.company_verifier import CompanyVerifier
from supplier_intelligence.rfq.quote_comparator import QuoteComparator
from supplier_intelligence.rfq.quote_normalizer import QuoteNormalizer
from supplier_intelligence.supplier_candidate import SupplierCandidate
from supplier_intelligence.supplier_discovery import SupplierDiscovery
from supplier_intelligence.supplier_risk_assessor import SupplierRiskAssessor
from supplier_intelligence.supplier_score import SupplierScore
from tax.province_rule_registry import ProvinceRuleRegistry
from tax.tax_reconciliation import TaxReconciliation


def test_supplier_discovery_risk_and_weighted_score():
    candidates=[SupplierCandidate("s1","Verified","CN",5,True,True),SupplierCandidate("s2","New","CN",.2,False,False)]
    assert [x.supplier_id for x in SupplierDiscovery().filter(candidates)]==["s1"]
    assert SupplierRiskAssessor().assess(candidates[1].__dict__ if hasattr(candidates[1],"__dict__") else {"verified":False,"trade_assurance":False,"years_active":.2}).score>=.5
    score=SupplierScore.calculate(quality=.9,delivery=.8,communication=.7,compliance=1,price=.6)
    assert .7<score.total<=1


def test_company_verifier_and_quote_ranking():
    assert CompanyVerifier().verify({"legal_name":"A","registration_id":"R","country_code":"CN"})[0]
    normalizer=QuoteNormalizer()
    quotes=[normalizer.normalize({"supplier":"a","unit_price":10,"freight":20,"quantity":10,"lead_time_days":8}),normalizer.normalize({"supplier":"b","unit_price":9,"freight":40,"quantity":10,"lead_time_days":5})]
    assert QuoteComparator().rank(quotes)[0]["supplier"]=="a"


def test_catalog_quality_gate():
    report=CatalogQualityGate().evaluate({"title":"Useful shelf","description":"x"*100,"price_cad":30,"landed_cost_cad":10,"stock":2,"images":["a"]})
    assert report["allowed"]
    assert not CatalogQualityGate().evaluate({"title":"","price_cad":5,"landed_cost_cad":10})["allowed"]


def test_return_policy_validation_and_label_plan():
    request=ReturnRequest("r1","o1","damaged",({"sku":"A","quantity":1},),datetime.now(timezone.utc))
    assert ReturnValidator().validate(request)[0]
    decision=RefundPolicy().decide(paid_cad=100,requested_cad=80,reason="damaged",delivered=True,days_since_delivery=5)
    assert decision.approved and decision.amount_cad==80
    assert ReturnLabelPlanner().plan(reason="damaged",item_value_cad=100,return_shipping_cad=10)=="merchant_paid_label"


def test_tax_rules_and_reconciliation():
    assert ProvinceRuleRegistry().rate("QC")==.14975
    assert TaxReconciliation().compare(15,15.03)["matched"]
    assert not TaxReconciliation().compare(15,16)["matched"]
