from __future__ import annotations


def compare_offers(offers: list[dict[str, object]], *, quantity: int, weights: dict[str, float] | None = None) -> list[dict[str, object]]:
    weights = weights or {"cost": 0.45, "delivery": 0.25, "supplier": 0.25, "moq": 0.05}
    ranked = []
    for offer in offers:
        price = float(offer.get("unit_cost", 0) or 0)
        shipping = float(offer.get("shipping_cost", 0) or 0)
        delivery_days = max(1.0, float(offer.get("delivery_days", 60) or 60))
        supplier_score = max(0.0, min(1.0, float(offer.get("supplier_score", 0.5) or 0.5)))
        moq = max(1, int(offer.get("moq", 1) or 1))
        landed = price * quantity + shipping
        score = (1 / (1 + landed)) * weights["cost"] + (1 / delivery_days) * weights["delivery"] + supplier_score * weights["supplier"] + (1.0 if quantity >= moq else 0.0) * weights["moq"]
        ranked.append({**offer, "landed_total": round(landed, 2), "comparison_score": round(score, 6), "eligible": quantity >= moq})
    return sorted(ranked, key=lambda item: (not bool(item["eligible"]), -float(item["comparison_score"])))
