from __future__ import annotations

from collections.abc import Callable
from typing import Any


class KPIRegistry:
    def __init__(self) -> None:
        self._functions: dict[str, Callable[[dict[str, Any]], float]] = {}

    def register(self, name: str, function: Callable[[dict[str, Any]], float]) -> None:
        self._functions[name] = function

    def calculate(self, facts: dict[str, Any]) -> dict[str, float]:
        return {name: float(function(facts)) for name, function in self._functions.items()}


def default_registry() -> KPIRegistry:
    registry = KPIRegistry()
    registry.register("conversion_rate", lambda f: f.get("orders", 0) / max(1, f.get("sessions", 0)))
    registry.register("average_order_value", lambda f: f.get("revenue", 0) / max(1, f.get("orders", 0)))
    registry.register("gross_margin", lambda f: (f.get("revenue", 0) - f.get("cogs", 0)) / max(1, f.get("revenue", 0)))
    registry.register("refund_rate", lambda f: f.get("refunds", 0) / max(1, f.get("orders", 0)))
    return registry
