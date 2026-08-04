from __future__ import annotations

import pytest

from domain.events.base_event import DomainEvent
from domain.events.order_events import order_event
from domain.state_machines.base import StateMachine, Transition
from domain.state_machines.payment_state_machine import PaymentStateMachine
from domain.state_machines.shopify_order_state_machine import ShopifyOrderStateMachine


def test_state_machine_introspection_path_and_terminal_states():
    machine = ShopifyOrderStateMachine()
    assert machine.can("received", "payment_confirmed")
    assert machine.path("received", "fulfilled") == ("payment_confirmed", "risk_clear", "procured", "fulfilled")
    assert machine.is_terminal("fulfilled")
    assert "received" in machine.states


def test_state_machine_apply_records_fingerprint_and_history():
    machine = PaymentStateMachine()
    result = machine.apply("pending", "authorize", {"transaction_id": "t1"})
    assert result.target == "authorized" and result.fingerprint
    assert machine.recent(1)[0] == result
    assert "capture" in machine.events("authorized")


def test_state_machine_guard_blocks_transition():
    machine = StateMachine([
        Transition("pending", "paid", "capture", guard=lambda context: bool(context.get("authorized")))
    ])
    assert not machine.can("pending", "capture", {"authorized": False})
    with pytest.raises(PermissionError):
        machine.transition("pending", "capture", {"authorized": False})
    assert machine.transition("pending", "capture", {"authorized": True}) == "paid"


def test_state_machine_rejects_duplicate_transition():
    with pytest.raises(ValueError, match="duplicate"):
        StateMachine([Transition("a", "b", "go"), Transition("a", "c", "go")])


def test_domain_event_normalizes_and_hashes():
    event = DomainEvent.create("Order", "Paid", {"id": 1})
    assert event.topic == "order.paid" and event.aggregate == "order" and event.action == "paid"
    assert len(event.fingerprint) == 24 and len(event.event_hash) == 64
    assert DomainEvent.from_dict(event.as_dict()).fingerprint == event.fingerprint


def test_domain_event_causation_and_factory():
    cause = order_event("received", {"id": 1})
    effect = order_event("paid", {"id": 1}).caused_by(cause)
    assert effect.causation_id == cause.id and effect.correlation_id == cause.id


def test_domain_event_rejects_invalid_topic_and_large_payload():
    with pytest.raises(ValueError):
        DomainEvent("bad", {})
    with pytest.raises(ValueError, match="volumineux"):
        DomainEvent("order.large", {"data": "x" * 1_000_001})
