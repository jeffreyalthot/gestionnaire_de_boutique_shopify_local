from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class StoreHealthWorkflow(BaseWorkflow):
    name = 'store_health'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('probe_integrations', self._step_0_probe_integrations, mutating=False, approval_required=False),
            WorkflowStep('probe_database', self._step_1_probe_database, mutating=False, approval_required=False),
            WorkflowStep('probe_queues', self._step_2_probe_queues, mutating=False, approval_required=False),
            WorkflowStep('publish_health', self._step_3_publish_health, mutating=True, approval_required=False),
        )

    def _step_0_probe_integrations(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'integrations_ok': bool(ctx.get('integrations_ok', True))}

    def _step_1_probe_database(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'database_ok': bool(ctx.get('database_ok', True))}

    def _step_2_probe_queues(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'queues_ok': int(ctx.get('failed_tasks', 0)) == 0}

    def _step_3_publish_health(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'healthy': all(bool(ctx.get(k)) for k in ('integrations_ok','database_ok','queues_ok'))}

