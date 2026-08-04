from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class OrderExceptionWorkflow(BaseWorkflow):
    name = 'order_exception'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('load_order', self._step_0_load_order, mutating=False, approval_required=False),
            WorkflowStep('classify_failure', self._step_1_classify_failure, mutating=False, approval_required=False),
            WorkflowStep('select_compensation', self._step_2_select_compensation, mutating=False, approval_required=False),
            WorkflowStep('execute_compensation', self._step_3_execute_compensation, mutating=True, approval_required=True),
        )

    def _step_0_load_order(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'order_loaded': bool(ctx.get('order_id'))}

    def _step_1_classify_failure(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'failure_category': str(ctx.get('failure_category', 'unknown'))}

    def _step_2_select_compensation(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'compensation': str(ctx.get('compensation', 'manual_review'))}

    def _step_3_execute_compensation(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'compensated': True}

