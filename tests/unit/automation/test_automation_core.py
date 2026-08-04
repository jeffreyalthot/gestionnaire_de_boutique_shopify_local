from __future__ import annotations

import asyncio

from automation.core.automation_state import AutomationState
from automation.core.capability_matrix import CapabilityMatrix
from automation.core.runtime_budget import ResourceGovernor, RuntimeBudget
from automation.decisions.decision_engine import DecisionEngine
from automation.execution.action_executor import ActionExecutor, ActionPlan
from automation.policies.policy_engine import ActionPolicy, PolicyEngine


def test_resource_governor_limits_heavy_operations():
    governor = ResourceGovernor(RuntimeBudget(max_heavy_operations_per_cycle=1))
    governor.begin_cycle("cycle")
    assert governor.allow(heavy=True)[0]
    assert governor.allow(heavy=True) == (False, "heavy_operation_budget_exhausted")


def test_automation_state_uses_fixed_counters():
    state = AutomationState()
    state.begin_cycle("abc")
    state.record("planned", "catalog")
    state.record("accepted", "catalog")
    snapshot = state.snapshot()
    assert snapshot["cycles"] == 1
    assert snapshot["planned"] == 1
    assert snapshot["accepted"] == 1
    assert snapshot["cycle_id"] == "abc"


def test_policy_engine_never_executes_finance_without_approval():
    engine = PolicyEngine(dry_run=False, financial_limit_cad=100)
    policy = ActionPolicy("purchase", risk="financial")
    assert not engine.evaluate(policy, amount_cad=50).allowed
    assert engine.evaluate(policy, amount_cad=50, approved=True).allowed
    assert not engine.evaluate(policy, amount_cad=101, approved=True).allowed


def test_action_executor_is_idempotent():
    calls = 0

    async def handler():
        nonlocal calls
        calls += 1
        return {"ok": True}

    executor = ActionExecutor(PolicyEngine(dry_run=False))
    plan = ActionPlan("inspect", "same", ActionPolicy("inspect"), handler)
    first = asyncio.run(executor.execute(plan))
    second = asyncio.run(executor.execute(plan))
    assert first.status == "completed"
    assert second.reason == "idempotent_replay"
    assert calls == 1


def test_decision_engine_is_deterministic():
    result = DecisionEngine().score({"margin": 0.9, "quality": 0.8}, {"margin": 0.6, "quality": 0.4}, threshold=0.7)
    assert result.accepted
    assert 0.0 <= result.confidence <= 1.0


def test_capabilities_are_available_in_dry_run(settings):
    matrix = CapabilityMatrix.from_settings(settings)
    assert matrix.allows("shopify.write")
    assert not matrix.allows("shopify.write", live=True)
