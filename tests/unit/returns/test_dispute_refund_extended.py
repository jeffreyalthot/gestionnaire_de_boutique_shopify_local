import pytest

from infrastructure.database.engine import Database
from returns.chargeback_evidence_builder import ChargebackEvidenceBuilder
from returns.exchange_planner import ExchangePlanner
from returns.refund_executor import RefundExecutor


def test_chargeback_builder_filters_unknown_evidence():
    items = ChargebackEvidenceBuilder().build({'tracking': 'X', 'password': 'secret'})
    assert [item.kind for item in items] == ['tracking']


def test_exchange_planner_enforces_stock_and_budget():
    planner = ExchangePlanner()
    assert planner.plan(replacement_sku='x', quantity=2, stock_available=1,
                        outbound_cost_cad=5, return_cost_cad=5, budget_cad=50).reason == 'insufficient_stock'


@pytest.mark.asyncio
async def test_refund_executor_is_idempotent(tmp_path):
    db = Database(tmp_path / 'db.sqlite'); db.initialize(); calls=[]
    async def remote_refund(**kwargs): calls.append(kwargs); return {'ok': True}
    executor = RefundExecutor(db, remote_refund)
    first = await executor.execute('o1', 20, 'k1', approved=True, dry_run=False)
    second = await executor.execute('o1', 20, 'k1', approved=True, dry_run=False)
    assert first.status == 'completed' and second.status == 'completed' and len(calls) == 1
