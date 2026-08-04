from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class DataQualityWorkflow(BaseWorkflow):
    name = 'data_quality'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('profile_records', self._step_0_profile_records, mutating=False, approval_required=False),
            WorkflowStep('detect_missing_fields', self._step_1_detect_missing_fields, mutating=False, approval_required=False),
            WorkflowStep('quarantine_invalid_records', self._step_2_quarantine_invalid_records, mutating=True, approval_required=False),
            WorkflowStep('publish_quality_score', self._step_3_publish_quality_score, mutating=True, approval_required=False),
        )

    def _step_0_profile_records(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'record_count': int(ctx.get('record_count', 0))}

    def _step_1_detect_missing_fields(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'missing_fields': tuple(ctx.get('missing_fields', ())) }

    def _step_2_quarantine_invalid_records(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'quarantined': int(ctx.get('invalid_count', 0))}

    def _step_3_publish_quality_score(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'quality_score': max(0.0, min(1.0, float(ctx.get('quality_score', 1.0))))}

