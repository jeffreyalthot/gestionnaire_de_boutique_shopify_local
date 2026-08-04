from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any

from integrations.alibaba.client import AlibabaClient
from integrations.alibaba.mappers.payment_mapper import map_payment


@dataclass(frozen=True, slots=True)
class PaymentResult:
    supplier_order_id: str
    status: str
    terminal: bool
    successful: bool
    retryable: bool
    external_reference: str
    checked_at: str
    raw: dict[str, object]

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class PaymentResultMonitor:
    TERMINAL = {"paid", "success", "completed", "failed", "cancelled", "refunded"}
    SUCCESS = {"paid", "success", "completed"}
    RETRYABLE = {"pending", "processing", "submitted", "timeout", "unknown"}

    def __init__(self, client: AlibabaClient) -> None:
        self.client = client
        self.checks = 0
        self.failures = 0

    async def inspect(self, order_id: str) -> PaymentResult:
        if not str(order_id).strip():
            raise ValueError("order_id requis")
        self.checks += 1
        try:
            mapped = map_payment(await self.client.payment_result(str(order_id)))
        except Exception:
            self.failures += 1
            raise
        status = str(mapped.get("status") or mapped.get("pay_status") or "unknown").strip().lower()
        reference = str(mapped.get("external_reference") or mapped.get("payment_id") or mapped.get("id") or "")
        return PaymentResult(
            supplier_order_id=str(order_id),
            status=status,
            terminal=status in self.TERMINAL,
            successful=status in self.SUCCESS,
            retryable=status in self.RETRYABLE,
            external_reference=reference,
            checked_at=datetime.now(timezone.utc).isoformat(),
            raw=dict(mapped),
        )

    async def check(self, order_id: str) -> dict[str, object]:
        return (await self.inspect(order_id)).raw

    async def wait_until_terminal(
        self,
        order_id: str,
        *,
        maximum_checks: int = 5,
        sleep: Any | None = None,
        delay_seconds: float = 1.0,
    ) -> PaymentResult:
        result: PaymentResult | None = None
        for attempt in range(max(1, int(maximum_checks))):
            result = await self.inspect(order_id)
            if result.terminal:
                return result
            if sleep is not None and attempt + 1 < maximum_checks:
                await sleep(max(0.0, float(delay_seconds)))
        assert result is not None
        return result

    def stats(self) -> dict[str, int]:
        return {"checks": self.checks, "failures": self.failures}
