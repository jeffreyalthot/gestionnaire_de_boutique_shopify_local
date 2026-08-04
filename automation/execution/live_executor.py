from __future__ import annotations

import asyncio

from automation.execution.action_plan import ActionPlan
from automation.execution.action_result import ActionResult


class LiveExecutor:
    async def execute(self, plan: ActionPlan) -> ActionResult:
        try:
            output = await asyncio.wait_for(plan.handler(), timeout=plan.timeout_seconds)
            return ActionResult(plan.name, "completed", plan.idempotency_key, False, "executed", output)
        except asyncio.TimeoutError:
            return ActionResult(plan.name, "failed", plan.idempotency_key, False, "timeout", error="operation_timeout")
        except Exception as exc:
            return ActionResult(plan.name, "failed", plan.idempotency_key, False, "handler_failed", error=f"{type(exc).__name__}: {exc}"[:1000])
