from __future__ import annotations

from typing import Any

from procurement.procurement_engine import ProcurementEngine


class ProcurementBatchWorkflow:
    def __init__(self, engine: ProcurementEngine) -> None:
        self.engine = engine

    async def execute(self) -> dict[str, object]:
        batch = self.engine.accumulate_paid_orders()
        decision = self.engine.evaluate_batch(batch)
        batch_id = str(getattr(batch, "id", "") or (batch.get("id", "") if isinstance(batch, dict) else ""))
        return {
            "batch": batch,
            "batch_id": batch_id,
            "decision": decision,
            "ready": bool(getattr(decision, "approved", False) or (decision.get("approved", False) if isinstance(decision, dict) else False)),
        }
