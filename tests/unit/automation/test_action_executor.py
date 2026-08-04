import pytest
from automation.execution.action_executor import ActionExecutor
from automation.execution.action_plan import ActionPlan
from automation.policies.policy_engine import ActionPolicy,PolicyEngine

@pytest.mark.asyncio
async def test_action_executor_simulates_mutation_in_dry_run():
    async def handler(): return {"live":True}
    plan=ActionPlan("publish","publish:1",ActionPolicy("publish",risk="external_write"),handler)
    result=await ActionExecutor(PolicyEngine(dry_run=True)).execute(plan)
    assert result.status=="completed" and result.simulated
