from __future__ import annotations


class UnpublishPlanner:
    def plan(self, product: dict[str, object]) -> dict[str, object]:
        reasons: list[str] = []
        if int(product.get("stock", 0) or 0) <= 0: reasons.append("out_of_stock")
        if float(product.get("margin_percent", 0.0) or 0.0) < 20: reasons.append("low_margin")
        if str(product.get("compliance_status", "passed")) != "passed": reasons.append("compliance")
        if not bool(product.get("supplier_active", True)): reasons.append("supplier_unavailable")
        return {"unpublish": bool(reasons), "reasons": tuple(reasons), "preserve_redirect": True}
