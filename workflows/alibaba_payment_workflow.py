from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

from procurement.payment_orchestrator import PaymentOrchestrator


class AlibabaPaymentWorkflow:
    def __init__(self, orchestrator: PaymentOrchestrator, *, maximum_amount_cad: float = 10_000.0) -> None:
        self.orchestrator = orchestrator
        self.maximum_amount_cad = Decimal(str(maximum_amount_cad))
        self.last_payment: dict[str, Any] | None = None

    async def execute(self, batch_id: str, order_id: str, amount: float, currency: str = "CAD") -> dict[str, object]:
        if not str(batch_id).strip() or not str(order_id).strip():
            raise ValueError("batch_id et order_id requis")
        try:
            normalized_amount = Decimal(str(amount)).quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Montant de paiement invalide") from exc
        if normalized_amount <= 0 or normalized_amount > self.maximum_amount_cad:
            raise ValueError("Montant de paiement hors politique")
        normalized_currency = str(currency).strip().upper()
        if len(normalized_currency) != 3:
            raise ValueError("Devise invalide")
        result = await self.orchestrator.pay(str(batch_id), str(order_id), float(normalized_amount), normalized_currency)
        self.last_payment = dict(result or {})
        return self.last_payment
