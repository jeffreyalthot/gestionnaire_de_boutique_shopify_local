from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class CustomerNotificationWorkflow(BaseWorkflow):
    name = 'customer_notification'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('resolve_customer_channel', self._step_0_resolve_customer_channel, mutating=False, approval_required=False),
            WorkflowStep('render_localized_message', self._step_1_render_localized_message, mutating=False, approval_required=False),
            WorkflowStep('apply_suppression_policy', self._step_2_apply_suppression_policy, mutating=False, approval_required=False),
            WorkflowStep('send_notification', self._step_3_send_notification, mutating=True, approval_required=False),
        )

    def _step_0_resolve_customer_channel(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'channel': str(ctx.get('channel', 'email'))}

    def _step_1_render_localized_message(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'message_ready': bool(ctx.get('template') or ctx.get('message'))}

    def _step_2_apply_suppression_policy(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'suppressed': bool(ctx.get('unsubscribed', False))}

    def _step_3_send_notification(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'sent': bool(ctx.get('message_ready')) and not bool(ctx.get('suppressed'))}

