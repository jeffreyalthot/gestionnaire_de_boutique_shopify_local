from __future__ import annotations

from typing import Any

from ai.agents.base_agent import PolicyAwareAgent


class PricingAgent(PolicyAwareAgent):
    """Valide le prix proposé, le coût rendu et la marge disponible."""

    description = "Valide prix, coût rendu et marge."
    positive_signals = ("margin_score", "price_freshness")
    negative_signals = ("cost_volatility", "competitor_gap")
    hard_block_signals = ("negative_margin", "stale_supplier_price")

    def prepare_context(self, context: dict[str, Any]) -> dict[str, Any]:
        value = dict(context)

        # Les signaux explicites du runtime ont priorité. Les valeurs dérivées ne
        # sont calculées que lorsque les données brutes nécessaires existent.
        has_price = value.get("price") not in (None, "")
        has_cost = value.get("landed_cost") not in (None, "")
        if has_price and has_cost:
            try:
                price = float(value["price"])
                cost = float(value["landed_cost"])
            except (TypeError, ValueError):
                price = 0.0
                cost = 0.0
            margin = (price - cost) / price if price > 0 else -1.0
            value.setdefault("margin_score", max(0.0, min(1.0, margin / 0.5)))
            value.setdefault("negative_margin", margin < 0.0)
        else:
            value.setdefault("negative_margin", False)

        if value.get("price_age_hours") not in (None, ""):
            try:
                age_hours = max(0.0, float(value["price_age_hours"]))
            except (TypeError, ValueError):
                age_hours = 0.0
            value.setdefault("price_freshness", max(0.0, 1.0 - age_hours / 168.0))
            value.setdefault("stale_supplier_price", age_hours > 168.0)
        else:
            value.setdefault("stale_supplier_price", False)

        return value
