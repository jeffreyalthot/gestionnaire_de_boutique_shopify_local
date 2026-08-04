from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from procurement.procurement_engine import ProcurementEngine


@dataclass(frozen=True, slots=True)
class AlibabaOrderWorkflowResult:
    batch_id: str
    status: str
    submitted_at: str
    result: dict[str, Any]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class AlibabaOrderWorkflow:
    def __init__(self, engine: ProcurementEngine) -> None:
        self.engine = engine
        self.last_result: AlibabaOrderWorkflowResult | None = None

    async def execute(self, batch_id: str) -> dict[str, object]:
        identifier = str(batch_id).strip()
        if not identifier:
            raise ValueError("batch_id requis")
        result = await self.engine.submit_batch(identifier)
        payload = dict(result or {})
        self.last_result = AlibabaOrderWorkflowResult(
            identifier,
            str(payload.get("status", "submitted")),
            datetime.now(timezone.utc).isoformat(),
            payload,
        )
        return payload
