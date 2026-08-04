from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class CashflowProtectionWorkflow(BaseWorkflow):
    name = 'cashflow_protection'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('calculate_exposure', self._step_0_calculate_exposure, mutating=False, approval_required=False),
            WorkflowStep('compare_reserve', self._step_1_compare_reserve, mutating=False, approval_required=False),
            WorkflowStep('freeze_optional_spend', self._step_2_freeze_optional_spend, mutating=True, approval_required=True),
        )

    def _step_0_calculate_exposure(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'exposure_cad': round(float(ctx.get('pending_supplier_cad', 0)) + float(ctx.get('refund_reserve_cad', 0)), 2)}

    def _step_1_compare_reserve(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'reserve_sufficient': float(ctx.get('cash_available_cad', 0)) >= float(ctx.get('exposure_cad', 0))}

    def _step_2_freeze_optional_spend(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'optional_spend_frozen': not bool(ctx.get('reserve_sufficient'))}

