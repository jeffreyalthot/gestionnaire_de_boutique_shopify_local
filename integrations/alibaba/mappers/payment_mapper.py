from __future__ import annotations

from decimal import Decimal


def map_payment(data: dict[str, object]) -> dict[str, object]:
    status = str(data.get("status") or data.get("payStatus") or "").lower()
    return {
        "status": status,
        "paid": status in {"paid", "success", "completed"},
        "reference": str(data.get("paymentId") or data.get("reference") or data.get("tradeNo") or ""),
        "order_id": str(data.get("orderId") or data.get("order_id") or ""),
        "amount": Decimal(str(data.get("amount") or data.get("paidAmount") or 0)),
        "currency": str(data.get("currency") or "USD"),
        "paid_at": str(data.get("paidAt") or data.get("payTime") or ""),
        "raw": data,
    }
