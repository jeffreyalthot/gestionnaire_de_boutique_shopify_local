from customers.privacy.consent_ledger import ConsentLedger
from pricing.price_snapshot_repository import PriceSnapshotRepository
from reports.operational_summary_report import OperationalSummaryReport
from reports.report_registry import ReportRegistry

def test_consent_ledger_records_revokes_and_audits(db):
    ledger=ConsentLedger(db);ledger.record(customer_id="c",purpose="marketing",granted=True,source="form");assert ledger.current("c","marketing");ledger.revoke("c","marketing",reason="request");assert not ledger.current("c","marketing") and ledger.audit("c")["record_count"]==2
def test_price_snapshot_volatility_and_change(db):
    repo=PriceSnapshotRepository(db);repo.record("product","p",price_cad=10,landed_cost_cad=5);repo.record("product","p",price_cad=12,landed_cost_cad=5);assert repo.change("product","p")["delta_cad"]==2 and repo.volatility("product","p")["samples"]==2
def test_report_registry_bundle(db):
    registry=ReportRegistry();registry.register("summary",OperationalSummaryReport);bundle=registry.bundle(["summary"],db);assert bundle["ok"] and "summary" in bundle["reports"]
