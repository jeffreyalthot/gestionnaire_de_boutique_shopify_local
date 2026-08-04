from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class RefundExecutionResult:
    order_id: str
    amount_cad: float
    status: str
    idempotency_key: str


class RefundExecutor:
    """Exécuteur protégé. L'appel distant est injecté et doit accepter une clé idempotente."""

    def __init__(self, db: Any, remote_refund: Any) -> None:
        self.db = db
        self.remote_refund = remote_refund

    async def execute(self, order_id: str, amount_cad: float, idempotency_key: str,
                      *, approved: bool, dry_run: bool = True) -> RefundExecutionResult:
        if amount_cad <= 0 or not idempotency_key:
            raise ValueError('Montant et clé idempotente requis.')
        existing = self.db.get_value(f'refund:{idempotency_key}', None)
        if existing:
            return RefundExecutionResult(**existing)
        if not approved:
            result = RefundExecutionResult(order_id, amount_cad, 'approval_required', idempotency_key)
        elif dry_run:
            result = RefundExecutionResult(order_id, amount_cad, 'simulated', idempotency_key)
        else:
            response = self.remote_refund(order_id=order_id, amount_cad=amount_cad,
                                          idempotency_key=idempotency_key)
            if hasattr(response, '__await__'):
                response = await response
            result = RefundExecutionResult(order_id, amount_cad,
                                           'completed' if response else 'failed', idempotency_key)
        self.db.set_value(f'refund:{idempotency_key}', asdict(result))
        return result
