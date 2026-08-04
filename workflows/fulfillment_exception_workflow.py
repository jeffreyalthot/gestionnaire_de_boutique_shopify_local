from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class FulfillmentExceptionWorkflow(BaseWorkflow):
    name = 'fulfillment_exception'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('classify_exception', self._step_0_classify_exception, mutating=False, approval_required=False),
            WorkflowStep('estimate_customer_impact', self._step_1_estimate_customer_impact, mutating=False, approval_required=False),
            WorkflowStep('select_recovery_action', self._step_2_select_recovery_action, mutating=False, approval_required=False),
            WorkflowStep('apply_recovery_action', self._step_3_apply_recovery_action, mutating=True, approval_required=True),
        )

    def _step_0_classify_exception(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'exception_type': str(ctx.get('exception_type', 'unknown'))}

    def _step_1_estimate_customer_impact(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'customer_impact': str(ctx.get('customer_impact', 'medium'))}

    def _step_2_select_recovery_action(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'recovery_action': str(ctx.get('recovery_action', 'investigate'))}

    def _step_3_apply_recovery_action(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'recovery_applied': True}

