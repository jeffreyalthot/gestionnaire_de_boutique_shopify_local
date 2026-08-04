from __future__ import annotations


class CustomerTagService:
    def build(self, *, lifetime_value_cad: float, order_count: int, risk_score: float,
              consented_marketing: bool) -> tuple[str, ...]:
        tags: set[str] = set()
        tags.add("vip" if lifetime_value_cad >= 1000 else ("repeat" if order_count >= 2 else "new"))
        if risk_score >= 0.50:
            tags.add("risk-review")
        if consented_marketing:
            tags.add("marketing-consented")
        return tuple(sorted(tags))
