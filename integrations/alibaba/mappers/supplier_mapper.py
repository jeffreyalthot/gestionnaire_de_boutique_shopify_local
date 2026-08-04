from __future__ import annotations


def map_supplier(data: dict[str, object]) -> dict[str, object]:
    return {
        "id": str(data.get("supplier_id") or data.get("memberId") or data.get("id") or ""),
        "name": str(data.get("company_name") or data.get("companyName") or data.get("name") or ""),
        "verified": bool(data.get("verified") or data.get("isVerified")),
        "years": max(0, int(data.get("years") or data.get("yearsOnAlibaba") or 0)),
        "country": str(data.get("country") or data.get("countryCode") or ""),
        "response_rate": float(data.get("responseRate") or data.get("response_rate") or 0),
        "on_time_delivery_rate": float(data.get("onTimeDeliveryRate") or data.get("on_time_delivery_rate") or 0),
        "trade_assurance": bool(data.get("tradeAssurance") or data.get("trade_assurance")),
        "raw": data,
    }
