from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class DiscountCampaignWorkflow(BaseWorkflow):
    name = 'discount_campaign'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('select_products', self._step_0_select_products, mutating=False, approval_required=False),
            WorkflowStep('verify_margin_floor', self._step_1_verify_margin_floor, mutating=False, approval_required=False),
            WorkflowStep('schedule_campaign', self._step_2_schedule_campaign, mutating=True, approval_required=True),
        )

    def _step_0_select_products(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'selected_products': tuple(ctx.get('product_ids', ())) }

    def _step_1_verify_margin_floor(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'margin_safe': float(ctx.get('post_discount_margin_percent', 0)) >= float(ctx.get('minimum_margin_percent', 40))}

    def _step_2_schedule_campaign(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'scheduled': bool(ctx.get('margin_safe'))}

