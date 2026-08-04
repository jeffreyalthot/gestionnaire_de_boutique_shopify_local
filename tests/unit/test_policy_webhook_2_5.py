from __future__ import annotations

import pytest

from automation.policies.policy_engine import ActionPolicy, PolicyEngine
from automation.policies.rule_policy import RulePolicy
from integrations.shopify.webhooks.handlers.base import HandlerPolicy, WebhookPayloadError, build_result
from integrations.shopify.webhooks.handlers.orders_paid import handle as handle_paid


def test_webhook_normalizes_gid_and_headers():
    result = handle_paid(
        {"id": "gid://shopify/Order/123", "created_at": "2026-07-30T12:00:00Z", "line_items": []},
        {
            "X-Shopify-Webhook-Id": "evt-1",
            "X-Shopify-Api-Version": "2026-07",
            "X-Shopify-Shop-Domain": "example.myshopify.com",
        },
    )
    assert result["entity_id"] == "123"
    assert result["event_id"] == "evt-1"
    assert result["source_version"] == "2026-07"
    assert result["shop_domain"] == "example.myshopify.com"
    assert result["payload_bytes"] > 0


def test_webhook_fingerprint_uses_full_payload():
    first = handle_paid({"id": 1, "created_at": "2026-01-01T00:00:00Z", "total": "10"})
    second = handle_paid({"id": 1, "created_at": "2026-01-01T00:00:00Z", "total": "11"})
    assert first["fingerprint"] != second["fingerprint"]


def test_webhook_marks_missing_and_timestamp_reconciliation():
    result = build_result(topic="orders/paid", action="paid", payload={}, required=("id",))
    assert result["requires_reconciliation"] is True
    assert "missing:id" in result["warnings"]
    assert "missing:entity_id" in result["warnings"]


def test_webhook_rejects_depth_and_size():
    with pytest.raises(WebhookPayloadError, match="depth"):
        build_result(topic="x/y", action="x", payload={"a": {"b": {"c": 1}}}, policy=HandlerPolicy(maximum_depth=1))
    with pytest.raises(WebhookPayloadError, match="too_large"):
        build_result(topic="x/y", action="x", payload={"a": "x" * 100}, policy=HandlerPolicy(maximum_payload_bytes=20))


def test_webhook_rejects_control_characters():
    with pytest.raises(WebhookPayloadError, match="control"):
        build_result(topic="x/y", action="x", payload={"value": "bad\x01value"})


def test_rule_policy_records_statistics_and_validators():
    policy = RulePolicy(minimum_score=0.8, validators=(lambda context: "blocked_country" if context.get("blocked") else None,))
    assert policy.evaluate(score=0.9).allowed
    denied = policy.evaluate(score=0.9, context={"blocked": True})
    assert not denied.allowed and denied.approval_required
    stats = policy.statistics()
    assert stats["evaluated"] == 2 and stats["allowed"] == 1


def test_rule_policy_allows_configured_violation_budget():
    policy = RulePolicy(minimum_score=0.5, maximum_violations=1)
    assert policy.evaluate(score=0.8, violations=("warning",)).allowed
    assert not policy.evaluate(score=0.8, violations=("a", "b")).allowed


def test_policy_engine_capability_and_mode_gates():
    engine = PolicyEngine(dry_run=False, capabilities={"read"}, mode="live")
    missing = engine.evaluate(ActionPolicy("sync", required_capabilities=("write",)))
    assert not missing.allowed and missing.reason == "missing_capability"
    blocked = engine.evaluate(ActionPolicy("sync", blocked_modes=("live",)))
    assert not blocked.allowed and blocked.reason == "mode_blocked"


def test_policy_engine_stale_financial_data_is_blocked():
    engine = PolicyEngine(dry_run=False)
    decision = engine.evaluate(ActionPolicy("purchase", risk="financial"), amount_cad=10, approved=True, context={"stale_data": True})
    assert not decision.allowed and decision.reason == "fresh_data_required"


def test_policy_engine_read_only_stale_data_is_warning():
    engine = PolicyEngine(dry_run=False)
    decision = engine.evaluate(ActionPolicy("read"), context={"stale_data": True})
    assert decision.allowed and "stale_data" in decision.warnings


def test_policy_engine_emergency_stop():
    engine = PolicyEngine(dry_run=True)
    decision = engine.evaluate(ActionPolicy("catalog-sync"), context={"emergency_stop": True})
    assert not decision.allowed and decision.reason == "emergency_stop"


def test_policy_engine_statistics_and_decision_id():
    engine = PolicyEngine(dry_run=True)
    decision = engine.evaluate(ActionPolicy("catalog-sync"))
    assert decision.decision_id and decision.evaluated_at
    assert engine.statistics()["simulated"] == 1
