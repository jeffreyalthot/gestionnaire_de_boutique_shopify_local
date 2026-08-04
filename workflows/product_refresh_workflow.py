from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class ProductRefreshWorkflow(BaseWorkflow):
    name = 'product_refresh'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('load_supplier_snapshot', self._step_0_load_supplier_snapshot, mutating=False, approval_required=False),
            WorkflowStep('calculate_change_set', self._step_1_calculate_change_set, mutating=False, approval_required=False),
            WorkflowStep('validate_change_set', self._step_2_validate_change_set, mutating=False, approval_required=False),
            WorkflowStep('apply_changes', self._step_3_apply_changes, mutating=True, approval_required=True),
        )

    def _step_0_load_supplier_snapshot(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'supplier_snapshot_loaded': bool(ctx.get('supplier_product_id'))}

    def _step_1_calculate_change_set(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'changes': tuple(ctx.get('changes', ())) }

    def _step_2_validate_change_set(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'changes_valid': not bool(ctx.get('unsafe_change', False))}

    def _step_3_apply_changes(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'changes_applied': len(ctx.get('changes', ())) if ctx.get('changes_valid') else 0}

