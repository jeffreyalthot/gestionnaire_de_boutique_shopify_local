from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class SupplierDueDiligenceWorkflow(BaseWorkflow):
    name = 'supplier_due_diligence'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('verify_identity', self._step_0_verify_identity, mutating=False, approval_required=False),
            WorkflowStep('verify_certifications', self._step_1_verify_certifications, mutating=False, approval_required=False),
            WorkflowStep('score_history', self._step_2_score_history, mutating=False, approval_required=False),
            WorkflowStep('approve_supplier', self._step_3_approve_supplier, mutating=True, approval_required=True),
        )

    def _step_0_verify_identity(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'identity_verified': bool(ctx.get('company_id'))}

    def _step_1_verify_certifications(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'certifications_verified': not bool(ctx.get('expired_certification', False))}

    def _step_2_score_history(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'history_score': max(0.0, min(1.0, float(ctx.get('history_score', 0))))}

    def _step_3_approve_supplier(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'approved_supplier': bool(ctx.get('identity_verified')) and bool(ctx.get('certifications_verified')) and float(ctx.get('history_score', 0)) >= 0.65}

