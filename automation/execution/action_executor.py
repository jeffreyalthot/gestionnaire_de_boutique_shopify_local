from __future__ import annotations

import asyncio
from typing import Any

from automation.execution.action_plan import ActionPlan
from automation.execution.action_result import ActionResult
from automation.policies.policy_engine import PolicyEngine


class ActionExecutor:
    def __init__(self, policy_engine: PolicyEngine, db: Any | None = None) -> None:
        self.policy_engine = policy_engine
        self.db = db
        self._memory_results: dict[str, ActionResult] = {}

    def _load(self, key: str) -> ActionResult | None:
        if key in self._memory_results:
            return self._memory_results[key]
        if self.db is None:
            return None
        row = self.db.query_one("SELECT result_json FROM automation_actions WHERE idempotency_key=? AND status='completed'", (key,))
        if not row:
            return None
        import json
        data = json.loads(row["result_json"])
        return ActionResult(**data)

    def _save(self, result: ActionResult) -> None:
        self._memory_results[result.idempotency_key] = result
        if self.db is None:
            return
        import json
        self.db.execute(
            "INSERT INTO automation_actions(id,idempotency_key,name,status,result_json,error,updated_at) VALUES(?,?,?,?,?,?,?) "
            "ON CONFLICT(idempotency_key) DO UPDATE SET status=excluded.status,result_json=excluded.result_json,error=excluded.error,updated_at=excluded.updated_at",
            (result.idempotency_key, result.idempotency_key, result.name, result.status, json.dumps(result.as_dict(), ensure_ascii=False, default=str), result.error, result.finished_at),
        )

    async def execute(self, plan: ActionPlan) -> ActionResult:
        cached = self._load(plan.idempotency_key)
        if cached is not None:
            cached.reason = "idempotent_replay"
            return cached
        decision = self.policy_engine.evaluate(plan.policy, amount_cad=plan.amount_cad, approved=plan.approved)
        if not decision.allowed:
            result = ActionResult(plan.name, "rejected", plan.idempotency_key, decision.simulated, decision.reason)
            self._save(result)
            return result
        if decision.simulated:
            result = ActionResult(plan.name, "completed", plan.idempotency_key, True, decision.reason, {"metadata": plan.metadata})
            self._save(result)
            return result
        try:
            output = await asyncio.wait_for(plan.handler(), timeout=plan.timeout_seconds)
            result = ActionResult(plan.name, "completed", plan.idempotency_key, False, decision.reason, output)
        except Exception as exc:
            result = ActionResult(plan.name, "failed", plan.idempotency_key, False, "handler_failed", error=f"{type(exc).__name__}: {exc}"[:1000])
        self._save(result)
        return result
