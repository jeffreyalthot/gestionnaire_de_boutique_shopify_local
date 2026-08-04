from __future__ import annotations

from typing import Any, Iterable

from workflows.base_workflow import BaseWorkflow, WorkflowStep


class EndOfMonthWorkflow(BaseWorkflow):
    name = 'end_of_month'

    def steps(self) -> Iterable[WorkflowStep]:
        return (
            WorkflowStep('lock_period_inputs', self._step_0_lock_period_inputs, mutating=False, approval_required=False),
            WorkflowStep('reconcile_ledger', self._step_1_reconcile_ledger, mutating=False, approval_required=False),
            WorkflowStep('recognize_reserves', self._step_2_recognize_reserves, mutating=False, approval_required=False),
            WorkflowStep('close_period', self._step_3_close_period, mutating=True, approval_required=True),
        )

    def _step_0_lock_period_inputs(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'inputs_locked': True}

    def _step_1_reconcile_ledger(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'ledger_balanced': bool(ctx.get('ledger_balanced', True))}

    def _step_2_recognize_reserves(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'reserves_recognized': True}

    def _step_3_close_period(self, ctx: dict[str, Any]) -> dict[str, Any]:
        return {'period_closed': bool(ctx.get('ledger_balanced'))}

