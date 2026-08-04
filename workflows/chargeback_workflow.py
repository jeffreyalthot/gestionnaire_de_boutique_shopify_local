from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class ChargebackWorkflow(BaseWorkflow):
    name = 'chargeback'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('load_order_evidence', self._step_0_load_order_evidence, mutating=False, approval_required=False),
            WorkflowStep('build_evidence_package', self._step_1_build_evidence_package, mutating=False, approval_required=False),
            WorkflowStep('risk_review', self._step_2_risk_review, mutating=False, approval_required=False),
            WorkflowStep('submit_response', self._step_3_submit_response, mutating=True, approval_required=True),
        )

    def _step_0_load_order_evidence(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'evidence_loaded': bool(ctx.get('order_id'))}

    def _step_1_build_evidence_package(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'evidence_items': len(ctx.get('evidence', []))}

    def _step_2_risk_review(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'submission_recommended': int(ctx.get('evidence_items', 0)) > 0}

    def _step_3_submit_response(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'response_submitted': bool(ctx.get('submission_recommended'))}

