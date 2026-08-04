from __future__ import annotations

from typing import Any

from analytics.attribution.channel_attribution import ChannelAttribution


class OrderAttribution:
    def __init__(self) -> None:
        self.channels = ChannelAttribution()

    def attribute(self, order: dict[str, Any], touchpoints: list[dict[str, Any]], *, model: str = "position_based") -> dict[str, Any]:
        revenue = float(order.get("revenue_cad", order.get("total_amount", 0.0)))
        return {"order_id": str(order.get("id", "")), "model": model,
                "revenue_cad": revenue, "allocation": self.channels.allocate(touchpoints, revenue, model=model)}
