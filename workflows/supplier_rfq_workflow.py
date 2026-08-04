from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class SupplierRfqWorkflow(BaseWorkflow):
    name = 'supplier_rfq'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('build_rfq', self._step_0_build_rfq, mutating=False, approval_required=False),
            WorkflowStep('select_suppliers', self._step_1_select_suppliers, mutating=False, approval_required=False),
            WorkflowStep('send_rfq', self._step_2_send_rfq, mutating=True, approval_required=True),
            WorkflowStep('compare_quotes', self._step_3_compare_quotes, mutating=False, approval_required=False),
        )

    def _step_0_build_rfq(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'rfq_ready': bool(ctx.get('product_id')) and int(ctx.get('quantity', 0)) > 0}

    def _step_1_select_suppliers(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'supplier_count': len(ctx.get('supplier_ids', []))}

    def _step_2_send_rfq(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'rfq_sent': int(ctx.get('supplier_count', 0)) if ctx.get('rfq_ready') else 0}

    def _step_3_compare_quotes(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'quotes_compared': len(ctx.get('quotes', []))}

