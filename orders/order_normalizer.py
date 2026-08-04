from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from orders.address_quality import AddressQuality


class OrderNormalizer:
    def normalize(self, raw: dict[str, object]) -> dict[str, object]:
        amount = Decimal(str(raw.get("total_amount", raw.get("total", 0)) or 0)).quantize(Decimal("0.01"), ROUND_HALF_UP)
        address = raw.get("shipping_address") if isinstance(raw.get("shipping_address"), dict) else {}
        lines=[]
        for line in raw.get("lines", []) if isinstance(raw.get("lines"), list) else []:
            if not isinstance(line, dict): continue
            lines.append({
                **line,
                "sku": str(line.get("sku", "")).strip().upper(),
                "quantity": max(0, int(line.get("quantity", 0) or 0)),
            })
        return {
            **raw,
            "id": str(raw.get("id") or raw.get("shopify_order_id") or ""),
            "total_amount": float(amount),
            "currency": str(raw.get("currency", "CAD")).upper(),
            "shipping_address": AddressQuality().evaluate(address).normalized,
            "lines": lines,
        }
