from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class EndOfDayWorkflow(BaseWorkflow):
    name = 'end_of_day'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('reconcile_orders', self._step_0_reconcile_orders, mutating=False, approval_required=False),
            WorkflowStep('reconcile_cash', self._step_1_reconcile_cash, mutating=False, approval_required=False),
            WorkflowStep('snapshot_kpis', self._step_2_snapshot_kpis, mutating=True, approval_required=False),
            WorkflowStep('close_day', self._step_3_close_day, mutating=True, approval_required=True),
        )

    def _step_0_reconcile_orders(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'orders_reconciled': int(ctx.get('orders', 0))}

    def _step_1_reconcile_cash(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'cash_reconciled': True}

    def _step_2_snapshot_kpis(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'kpis_snapshotted': True}

    def _step_3_close_day(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'day_closed': True}

