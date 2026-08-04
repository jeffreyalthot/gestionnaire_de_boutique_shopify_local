from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class AlibabaMediaImportWorkflow(BaseWorkflow):
    name = 'alibaba_media_import'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('validate_source', self._step_0_validate_source, mutating=False, approval_required=False),
            WorkflowStep('download_and_validate', self._step_1_download_and_validate, mutating=True, approval_required=False),
            WorkflowStep('cache_media', self._step_2_cache_media, mutating=True, approval_required=False),
            WorkflowStep('stage_shopify_media', self._step_3_stage_shopify_media, mutating=True, approval_required=True),
        )

    def _step_0_validate_source(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'source_valid': bool(ctx.get('source_url') or ctx.get('images'))}

    def _step_1_download_and_validate(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'downloaded': len(ctx.get('images', []))}

    def _step_2_cache_media(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'cached': int(ctx.get('downloaded', 0))}

    def _step_3_stage_shopify_media(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'staged': int(ctx.get('cached', 0))}

