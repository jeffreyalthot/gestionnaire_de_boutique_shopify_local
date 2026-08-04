from __future__ import annotations

from decimal import Decimal


def map_order(data: dict[str, object]) -> dict[str, object]:
    lines = data.get("lines", data.get("orderLines", data.get("productItems", []))) or []
    return {
        "order_id": str(data.get("order_id") or data.get("orderId") or data.get("id") or ""),
        "status": str(data.get("status") or data.get("orderStatus") or "").lower(),
        "amount": Decimal(str(data.get("amount") or data.get("totalAmount") or 0)),
        "currency": str(data.get("currency") or data.get("currencyCode") or "USD"),
        "supplier_id": str(data.get("supplierId") or data.get("sellerMemberId") or ""),
        "created_at": str(data.get("createdAt") or data.get("createTime") or ""),
        "updated_at": str(data.get("updatedAt") or data.get("modifyTime") or ""),
        "lines": [dict(item) for item in lines if isinstance(item, dict)],
        "raw": data,
    }
