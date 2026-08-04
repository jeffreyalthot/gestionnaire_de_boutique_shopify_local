from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class SampleOrderWorkflow(BaseWorkflow):
    name = 'sample_order'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('validate_supplier', self._step_0_validate_supplier, mutating=False, approval_required=False),
            WorkflowStep('calculate_sample_budget', self._step_1_calculate_sample_budget, mutating=False, approval_required=False),
            WorkflowStep('request_sample', self._step_2_request_sample, mutating=True, approval_required=True),
        )

    def _step_0_validate_supplier(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'supplier_eligible': float(ctx.get('supplier_score', 0)) >= float(ctx.get('minimum_supplier_score', 0.65))}

    def _step_1_calculate_sample_budget(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'within_budget': float(ctx.get('sample_total_cad', 0)) <= float(ctx.get('sample_budget_cad', 0))}

    def _step_2_request_sample(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'sample_requested': bool(ctx.get('supplier_eligible')) and bool(ctx.get('within_budget'))}

