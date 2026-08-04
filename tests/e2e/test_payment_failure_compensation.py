import pytest
from automation.execution.action_executor import ActionExecutor
from automation.execution.action_plan import ActionPlan
from automation.policies.policy_engine import ActionPolicy,PolicyEngine

@pytest.mark.asyncio
async def test_failed_payment_is_recorded_and_idempotent():
    async def fail(): raise RuntimeError("payment refused")
    plan=ActionPlan("supplier-payment","pay:1",ActionPolicy("pay",risk="read_only"),fail)
    executor=ActionExecutor(PolicyEngine(dry_run=False))
    first=await executor.execute(plan); second=await executor.execute(plan)
    assert first.status=="failed" and second.reason=="idempotent_replay"
