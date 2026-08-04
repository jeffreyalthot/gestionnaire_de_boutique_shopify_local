from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any

from automation.core.automation_context import AutomationContext
from automation.core.automation_cycle import AutomationCycle
from automation.core.automation_state import AutomationState
from automation.core.capability_matrix import CapabilityMatrix
from automation.core.operation_registry import OperationDefinition, OperationRegistry
from automation.core.runtime_budget import ResourceGovernor


class AutomationSupervisor:
    def __init__(self, *, registry: OperationRegistry, capabilities: CapabilityMatrix,
                 governor: ResourceGovernor, state: AutomationState, queue: Any, db: Any,
                 dry_run: bool) -> None:
        self.registry = registry
        self.capabilities = capabilities
        self.governor = governor
        self.state = state
        self.queue = queue
        self.db = db
        self.dry_run = dry_run

    @staticmethod
    def _bucket_key(operation: str, interval_seconds: int, now: datetime) -> str:
        bucket = int(now.timestamp()) // max(1, interval_seconds)
        return sha256(f"automation:{operation}:{bucket}".encode()).hexdigest()

    def _last_queued(self, operation: str) -> datetime | None:
        value = self.db.get_value(f"automation:last-queued:{operation}")
        if not value:
            return None
        try:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError:
            return None

    def _due(self, definition: OperationDefinition, now: datetime, force: bool) -> tuple[bool, str]:
        if force:
            return True, "forced"
        last = self._last_queued(definition.name)
        if last is None:
            return True, "first_run"
        due_at = last + timedelta(seconds=max(1, definition.interval_seconds))
        if now >= due_at:
            return True, "interval_elapsed"
        return False, due_at.isoformat()

    async def run_cycle(self, *, force: bool = False) -> dict[str, Any]:
        context = AutomationContext(
            dry_run=self.dry_run,
            mode="dry_run" if self.dry_run else "supervised_live",
        )
        cycle = AutomationCycle(context)
        self.state.begin_cycle(context.cycle_id)
        self.governor.begin_cycle(context.cycle_id)
        pending = sum(self.queue.stats().get(status, 0) for status in ("pending", "leased"))
        self.state.set_phase("planning")
        now = datetime.now(timezone.utc)

        for definition in self.registry.all():
            cycle.report.planned += 1
            self.state.record("planned", definition.name)
            due, due_reason = self._due(definition, now, force)
            if not due:
                cycle.report.deferred += 1
                self.state.record("deferred", definition.name)
                cycle.report.operations.append({
                    "name": definition.name,
                    "status": "deferred",
                    "reason": "interval_not_elapsed",
                    "due_at": due_reason,
                })
                continue
            if not self.capabilities.allows(definition.capability, live=not self.dry_run):
                cycle.report.rejected += 1
                self.state.record("rejected", definition.name)
                cycle.report.operations.append({
                    "name": definition.name,
                    "status": "rejected",
                    "reason": "capability_unavailable",
                })
                continue
            allowed, reason = self.governor.allow(heavy=definition.heavy, pending_tasks=pending)
            if not allowed:
                cycle.report.deferred += 1
                self.state.record("deferred", definition.name)
                cycle.report.operations.append({"name": definition.name, "status": "deferred", "reason": reason})
                continue
            key = self._bucket_key(definition.name, definition.interval_seconds, now)
            task_id = self.queue.enqueue(
                "automation_operation",
                {
                    "operation": definition.name,
                    "cycle_id": context.cycle_id,
                    "dry_run": self.dry_run,
                    "scheduled_at": now.isoformat(),
                    "schedule_reason": due_reason,
                },
                key,
                queue=definition.queue,
                priority=definition.priority,
                max_attempts=6,
            )
            self.db.set_value(f"automation:last-queued:{definition.name}", now.isoformat())
            pending += 1
            cycle.report.accepted += 1
            self.state.record("accepted", definition.name)
            cycle.report.operations.append({"name": definition.name, "status": "queued", "task_id": task_id})

        self.state.set_phase("queued")
        cycle.report.finish()
        self.db.execute(
            "INSERT INTO automation_cycles(id,status,report_json,started_at,finished_at) VALUES(?,?,?,?,?)",
            (
                context.cycle_id,
                "queued",
                json.dumps(cycle.report.as_dict(), ensure_ascii=False),
                context.started_at,
                cycle.report.finished_at,
            ),
        )
        return cycle.report.as_dict()
