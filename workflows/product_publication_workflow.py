from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class ProductPublicationWorkflow(BaseWorkflow):
    name = 'product_publication'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('quality_gate', self._step_0_quality_gate, mutating=False, approval_required=False),
            WorkflowStep('compliance_gate', self._step_1_compliance_gate, mutating=False, approval_required=False),
            WorkflowStep('media_gate', self._step_2_media_gate, mutating=False, approval_required=False),
            WorkflowStep('publish_product', self._step_3_publish_product, mutating=True, approval_required=True),
        )

    def _step_0_quality_gate(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'quality_passed': float(ctx.get('quality_score', 0)) >= float(ctx.get('minimum_score', 0.68))}

    def _step_1_compliance_gate(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'compliance_passed': not bool(ctx.get('restricted', False))}

    def _step_2_media_gate(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'media_passed': int(ctx.get('media_count', 0)) > 0}

    def _step_3_publish_product(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'published': all(bool(ctx.get(k)) for k in ('quality_passed','compliance_passed','media_passed'))}

