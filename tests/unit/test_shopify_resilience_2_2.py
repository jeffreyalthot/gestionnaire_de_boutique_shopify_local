from __future__ import annotations
from datetime import datetime, timezone
import pytest
from integrations.shopify.graphql_cost_budget import GraphqlCostBudget
from integrations.shopify.pagination import paginate
from integrations.shopify.webhooks.reconciliation_cursor import ReconciliationCursor
from integrations.shopify.webhooks.sequence_guard import WebhookSequenceGuard

def test_graphql_budget_observes_reserves_and_restores():
    budget = GraphqlCostBudget(minimum_available=100, maximum_requested=1000)
    budget.observe({"cost":{"requestedQueryCost":20,"actualQueryCost":18,"throttleStatus":{"maximumAvailable":1000,"currentlyAvailable":150,"restoreRate":50}}})
    assert not budget.allows(60)
    assert budget.seconds_until_available(60) > 0
    assert budget.allows(40)
    assert budget.reserve(40)

def test_pagination_detects_cursor_loop():
    async def fetch(cursor):
        return {"edges":[],"pageInfo":{"hasNextPage":True,"endCursor":"same"}}
    async def consume():
        return [item async for item in paginate(fetch, max_pages=3)]
    with pytest.raises(RuntimeError, match="Boucle"):
        import asyncio; asyncio.run(consume())

def test_pagination_yields_nodes():
    async def fetch(cursor):
        return {"edges":[{"node":{"id":"1"}}],"pageInfo":{"hasNextPage":False,"endCursor":None}}
    async def consume():
        return [item async for item in paginate(fetch)]
    import asyncio
    assert asyncio.run(consume()) == [{"id":"1"}]

def test_webhook_sequence_guard_rejects_older_event():
    guard = WebhookSequenceGuard()
    assert guard.evaluate("order:1", "2026-07-30T01:00:00Z").process
    decision = guard.evaluate("order:1", "2026-07-29T23:00:00Z")
    assert decision.stale and not decision.process

def test_reconciliation_cursor_overlaps(db):
    cursor = ReconciliationCursor(db, "orders", overlap_minutes=5)
    cursor.commit(datetime(2026, 7, 30, 1, 0, tzinfo=timezone.utc))
    window = cursor.window(now=datetime(2026, 7, 30, 2, 0, tzinfo=timezone.utc))
    assert window.start.isoformat().startswith("2026-07-30T00:55")
    assert "updated_at:>=" in window.query_filter
