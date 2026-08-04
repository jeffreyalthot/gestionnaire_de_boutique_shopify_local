from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class SeoMaintenanceWorkflow(BaseWorkflow):
    name = 'seo_maintenance'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('scan_catalog', self._step_0_scan_catalog, mutating=False, approval_required=False),
            WorkflowStep('detect_seo_gaps', self._step_1_detect_seo_gaps, mutating=False, approval_required=False),
            WorkflowStep('prepare_updates', self._step_2_prepare_updates, mutating=False, approval_required=False),
            WorkflowStep('apply_updates', self._step_3_apply_updates, mutating=True, approval_required=True),
        )

    def _step_0_scan_catalog(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'products_scanned': int(ctx.get('products', 0))}

    def _step_1_detect_seo_gaps(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'gaps': int(ctx.get('gaps', 0))}

    def _step_2_prepare_updates(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'updates_prepared': int(ctx.get('gaps', 0))}

    def _step_3_apply_updates(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'updates_applied': int(ctx.get('updates_prepared', 0))}

