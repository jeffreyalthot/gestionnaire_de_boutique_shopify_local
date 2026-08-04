from __future__ import annotations

from collections import defaultdict


class SupplierPerformanceMonitor:
    def aggregate(self, shipments: list[dict[str, object]]) -> dict[str, dict[str, float]]:
        grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
        for shipment in shipments:
            grouped[str(shipment.get("supplier_id", "unknown"))].append(shipment)
        result = {}
        for supplier_id, items in grouped.items():
            count = len(items)
            on_time = sum(1 for item in items if bool(item.get("on_time"))) / count
            defects = sum(float(item.get("defect_rate", 0) or 0) for item in items) / count
            result[supplier_id] = {"shipments": float(count), "on_time": on_time, "defect_rate": defects}
        return result
