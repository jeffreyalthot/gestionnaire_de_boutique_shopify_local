from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class CustomerServiceWorkflow(BaseWorkflow):
    name = 'customer_service'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('classify_ticket', self._step_0_classify_ticket, mutating=False, approval_required=False),
            WorkflowStep('attach_order_context', self._step_1_attach_order_context, mutating=False, approval_required=False),
            WorkflowStep('prepare_response', self._step_2_prepare_response, mutating=False, approval_required=False),
            WorkflowStep('send_or_escalate', self._step_3_send_or_escalate, mutating=True, approval_required=False),
        )

    def _step_0_classify_ticket(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'category': str(ctx.get('category', 'general'))}

    def _step_1_attach_order_context(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'order_context_attached': bool(ctx.get('order_id'))}

    def _step_2_prepare_response(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'response_ready': True}

    def _step_3_send_or_escalate(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'escalated': bool(ctx.get('high_risk', False)), 'sent': not bool(ctx.get('high_risk', False))}

