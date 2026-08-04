from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class ShopifyStagedMediaWorkflow(BaseWorkflow):
    name = 'shopify_staged_media'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('validate_media_manifest', self._step_0_validate_media_manifest, mutating=False, approval_required=False),
            WorkflowStep('request_staged_targets', self._step_1_request_staged_targets, mutating=True, approval_required=False),
            WorkflowStep('upload_media', self._step_2_upload_media, mutating=True, approval_required=False),
            WorkflowStep('attach_media', self._step_3_attach_media, mutating=True, approval_required=True),
        )

    def _step_0_validate_media_manifest(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'manifest_valid': bool(ctx.get('media'))}

    def _step_1_request_staged_targets(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'staged_targets': len(ctx.get('media', []))}

    def _step_2_upload_media(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'uploaded': int(ctx.get('staged_targets', 0))}

    def _step_3_attach_media(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'attached': int(ctx.get('uploaded', 0))}

