from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowError, WorkflowStep


class FullStoreAutomationWorkflow(BaseWorkflow):
    """Top-level bounded workflow coordinating one complete store cycle."""

    name = "full_store_automation"

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep("health_gate", self._health_gate, timeout_seconds=20),
            WorkflowStep("resource_gate", self._resource_gate),
            WorkflowStep("commerce_cycle", self._commerce_cycle, timeout_seconds=120, retry_limit=1),
            WorkflowStep("reconciliation_cycle", self._reconciliation_cycle, timeout_seconds=60),
            WorkflowStep("maintenance_cycle", self._maintenance_cycle, mutating=True, timeout_seconds=60),
            WorkflowStep("final_snapshot", self._final_snapshot, timeout_seconds=30),
        )

    async def _health_gate(self, ctx: dict[str, Any]) -> dict[str, Any]:
        if self.container is None:
            healthy = bool(ctx.get("healthy", True))
            if not healthy:
                raise WorkflowError("runtime_unhealthy")
            return {"healthy": True, "health_status": "provided"}
        snapshot = await self.container.health.collect()
        if snapshot.get("status") == "unhealthy":
            raise WorkflowError("runtime_unhealthy")
        return {"healthy": True, "health_status": snapshot.get("status"), "health": snapshot}

    def _resource_gate(self, ctx: dict[str, Any]) -> dict[str, Any]:
        if self.container is None:
            return {"resources_allowed": bool(ctx.get("healthy", True))}
        resource = self.container.resource_governor.sample(cache_seconds=0.0)
        if not resource.get("within_memory_budget"):
            raise WorkflowError("memory_budget_exceeded")
        if not resource.get("within_cpu_budget"):
            raise WorkflowError("cpu_budget_exceeded")
        return {"resources_allowed": True, "resource": resource}

    async def _commerce_cycle(self, ctx: dict[str, Any]) -> dict[str, Any]:
        if not ctx.get("resources_allowed"):
            raise WorkflowError("resource_gate_not_passed")
        if self.container is None:
            return {"commerce_cycle_ready": True}
        report = await self.container.automation.run_cycle(force=bool(ctx.get("force", False)))
        return {"commerce_cycle_ready": True, "automation_report": report}

    def _reconciliation_cycle(self, ctx: dict[str, Any]) -> dict[str, Any]:
        if not ctx.get("commerce_cycle_ready"):
            raise WorkflowError("commerce_cycle_not_ready")
        if self.container is None:
            return {"reconciliation_ready": True}
        return {
            "reconciliation_ready": True,
            "queue": self.container.queue.stats(),
            "finance": self.container.db.financial_snapshot(),
            "audit": self.container.db.verify_audit_chain(),
        }

    def _maintenance_cycle(self, ctx: dict[str, Any]) -> dict[str, Any]:
        if not ctx.get("reconciliation_ready"):
            raise WorkflowError("reconciliation_not_ready")
        if self.container is None:
            return {"maintenance_completed": True}
        purged = self.container.queue.purge_completed(older_than_seconds=86_400, limit=1_000)
        oauth_purged = self.container.oauth_states.purge_expired() if hasattr(self.container.oauth_states, "purge_expired") else 0
        return {"maintenance_completed": True, "tasks_purged": purged, "oauth_states_purged": oauth_purged}

    async def _final_snapshot(self, ctx: dict[str, Any]) -> dict[str, Any]:
        if self.container is None or self.container.runtime_coordinator is None:
            return {"snapshot_created": False}
        snapshot = await self.container.runtime_coordinator.snapshot(persist=True)
        return {"snapshot_created": True, "runtime_snapshot": snapshot.as_dict()}
