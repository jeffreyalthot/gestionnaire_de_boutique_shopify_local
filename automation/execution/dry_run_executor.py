from __future__ import annotations

from automation.execution.action_plan import ActionPlan
from automation.execution.action_result import ActionResult


class DryRunExecutor:
    async def execute(self, plan: ActionPlan) -> ActionResult:
        return ActionResult(plan.name, "completed", plan.idempotency_key, True, "dry_run", {"metadata": plan.metadata, "amount_cad": plan.amount_cad})
