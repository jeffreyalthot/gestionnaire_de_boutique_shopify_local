from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class ApiVersionUpgradeWorkflow(BaseWorkflow):
    name = 'api_version_upgrade'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('inspect_current_version', self._step_0_inspect_current_version, mutating=False, approval_required=False),
            WorkflowStep('run_contract_tests', self._step_1_run_contract_tests, mutating=False, approval_required=False),
            WorkflowStep('prepare_migration', self._step_2_prepare_migration, mutating=False, approval_required=False),
            WorkflowStep('activate_version', self._step_3_activate_version, mutating=True, approval_required=True),
        )

    def _step_0_inspect_current_version(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'current_version': str(ctx.get('current_version', 'unknown'))}

    def _step_1_run_contract_tests(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'contract_tests_required': True}

    def _step_2_prepare_migration(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'target_version': str(ctx.get('target_version', ''))}

    def _step_3_activate_version(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'activated': str(ctx.get('target_version', ''))}

