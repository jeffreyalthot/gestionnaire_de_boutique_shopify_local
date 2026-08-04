from __future__ import annotations

from customers.customer_consent import CustomerConsent
from customers.customer_identity_resolver import CustomerIdentityResolver
from customers.customer_profile import CustomerProfile
from customers.customer_repository import CustomerRepository
from customers.customer_risk_profile import CustomerRiskProfiler
from customers.privacy.customer_export import CustomerExport
from customers.privacy.customer_redaction import CustomerRedaction
from customers.segments.segment_builder import SegmentBuilder


def test_customer_identity_is_hashed_and_normalized():
    resolver = CustomerIdentityResolver("secret")
    left = resolver.email_hash(" User@Example.com ")
    right = resolver.email_hash("user@example.com")
    assert left == right
    assert "user" not in left


def test_customer_repository_round_trip(db):
    repo = CustomerRepository(db)
    profile = CustomerProfile("c1", email_hash="hash", country_code="CA", language="fr",
                              lifetime_value_cad=123.45, risk_score=0.2,
                              preferences={"currency": "CAD"}, tags=("repeat",))
    repo.save(profile)
    loaded = repo.get("c1")
    assert loaded is not None
    assert loaded.lifetime_value_cad == 123.45
    assert loaded.tags == ("repeat",)


def test_consent_ledger_uses_latest_decision(db):
    consent = CustomerConsent(db)
    consent.record(customer_id="c1", purpose="marketing", granted=True, source="checkout")
    assert consent.current("c1", "marketing")
    consent.record(customer_id="c1", purpose="marketing", granted=False, source="account")
    assert not consent.current("c1", "marketing")


def test_customer_risk_and_segments_are_deterministic(db):
    risk = CustomerRiskProfiler().evaluate(chargebacks=1, refunds=2, orders=4, failed_payments=3)
    assert risk.level in {"high", "critical"}
    memberships = SegmentBuilder(db).build("c1", lifetime_value_cad=1200, order_count=10,
                                           risk_score=risk.score, days_since_last_order=20)
    assert {item["segment"] for item in memberships} >= {"value:gold", "retention:active"}


def test_export_and_redaction_remove_customer_identifiers(db):
    repo = CustomerRepository(db)
    repo.save(CustomerProfile("c1", email_hash="sensitive-hash", country_code="CA"))
    before = CustomerExport(db).build("c1")
    assert before["profile"]["email_hash"] == "sensitive-hash"
    CustomerRedaction(db).redact("c1")
    after = CustomerExport(db).build("c1")
    assert after["profile"]["email_hash"] == ""
    assert db.verify_audit_chain()["ok"]
