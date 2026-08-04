from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class CapabilityRefreshWorkflow(BaseWorkflow):
    name = 'capability_refresh'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('inspect_credentials', self._step_0_inspect_credentials, mutating=False, approval_required=False),
            WorkflowStep('probe_read_capabilities', self._step_1_probe_read_capabilities, mutating=False, approval_required=False),
            WorkflowStep('probe_write_scopes', self._step_2_probe_write_scopes, mutating=False, approval_required=False),
            WorkflowStep('persist_capabilities', self._step_3_persist_capabilities, mutating=True, approval_required=False),
        )

    def _step_0_inspect_credentials(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'credentials_present': bool(ctx.get('credentials_present', False))}

    def _step_1_probe_read_capabilities(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'read_capabilities_checked': True}

    def _step_2_probe_write_scopes(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'write_scopes_checked': True}

    def _step_3_persist_capabilities(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'capabilities_persisted': True}

