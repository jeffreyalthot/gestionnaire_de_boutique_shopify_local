from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class DisputeWorkflow(BaseWorkflow):
    name = 'dispute'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('classify_dispute', self._step_0_classify_dispute, mutating=False, approval_required=False),
            WorkflowStep('collect_documents', self._step_1_collect_documents, mutating=False, approval_required=False),
            WorkflowStep('build_response', self._step_2_build_response, mutating=False, approval_required=False),
            WorkflowStep('submit_dispute', self._step_3_submit_dispute, mutating=True, approval_required=True),
        )

    def _step_0_classify_dispute(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'dispute_type': str(ctx.get('dispute_type', 'unknown'))}

    def _step_1_collect_documents(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'documents': len(ctx.get('documents', []))}

    def _step_2_build_response(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'response_ready': int(ctx.get('documents', 0)) > 0}

    def _step_3_submit_dispute(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'submitted': bool(ctx.get('response_ready'))}

