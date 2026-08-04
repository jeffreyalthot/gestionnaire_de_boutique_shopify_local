from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from threading import RLock
from time import time
from typing import Mapping


@dataclass(frozen=True, slots=True)
class PaymentAttempt:
    key: str
    supplier_order_id: str
    amount: str
    currency: str
    status: str
    external_reference: str = ""
    created_at: float = 0.0
    updated_at: float = 0.0

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class PaymentIdempotency:
    def __init__(self, maximum_entries: int = 10_000) -> None:
        self.maximum_entries = max(10, int(maximum_entries))
        self._attempts: dict[str, PaymentAttempt] = {}
        self._lock = RLock()

    @staticmethod
    def _money(value: float | str | Decimal) -> Decimal:
        try:
            return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("Montant de paiement invalide") from exc

    def key(
        self,
        *,
        supplier_order_id: str,
        amount: float | str | Decimal,
        currency: str,
        payment_method_reference: str = "",
        metadata: Mapping[str, object] | None = None,
    ) -> str:
        order_id = str(supplier_order_id).strip()
        if not order_id:
            raise ValueError("supplier_order_id requis")
        normalized = {
            "supplier_order_id": order_id,
            "amount": format(self._money(amount), "f"),
            "currency": str(currency or "CAD").upper(),
            "payment_method_reference": str(payment_method_reference).strip(),
            "metadata": dict(sorted((metadata or {}).items())),
        }
        material = json.dumps(normalized, sort_keys=True, separators=(",", ":"), default=str)
        return "supplier-payment:" + hashlib.sha256(material.encode("utf-8")).hexdigest()

    def begin(self, **kwargs: object) -> PaymentAttempt:
        key = self.key(**kwargs)
        now = time()
        with self._lock:
            existing = self._attempts.get(key)
            if existing:
                return existing
            attempt = PaymentAttempt(
                key=key,
                supplier_order_id=str(kwargs["supplier_order_id"]),
                amount=format(self._money(kwargs["amount"]), "f"),
                currency=str(kwargs.get("currency") or "CAD").upper(),
                status="pending",
                created_at=now,
                updated_at=now,
            )
            self._attempts[key] = attempt
            self._trim_locked()
            return attempt

    def complete(self, key: str, *, status: str, external_reference: str = "") -> PaymentAttempt:
        normalized_status = str(status).strip().lower()
        if normalized_status not in {"paid", "submitted", "failed", "cancelled", "refunded", "unknown"}:
            raise ValueError("Statut de paiement invalide")
        with self._lock:
            current = self._attempts.get(key)
            if current is None:
                raise KeyError(key)
            updated = PaymentAttempt(
                key=current.key,
                supplier_order_id=current.supplier_order_id,
                amount=current.amount,
                currency=current.currency,
                status=normalized_status,
                external_reference=str(external_reference),
                created_at=current.created_at,
                updated_at=time(),
            )
            self._attempts[key] = updated
            return updated

    def get(self, key: str) -> PaymentAttempt | None:
        with self._lock:
            return self._attempts.get(key)

    def _trim_locked(self) -> None:
        overflow = len(self._attempts) - self.maximum_entries
        if overflow <= 0:
            return
        for key, _ in sorted(self._attempts.items(), key=lambda item: item[1].updated_at)[:overflow]:
            self._attempts.pop(key, None)
