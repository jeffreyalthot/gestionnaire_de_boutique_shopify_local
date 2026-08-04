from __future__ import annotations


class InventoryAssetValuation:
    def value(self, items: list[dict[str, object]], method: str = "weighted_average") -> dict[str, float]:
        if method not in {"weighted_average", "fifo_proxy"}:
            raise ValueError("Méthode de valorisation invalide.")
        total_units = sum(max(0, int(item.get("quantity", item.get("stock", 0)) or 0)) for item in items)
        total_cost = sum(max(0, int(item.get("quantity", item.get("stock", 0)) or 0)) * max(0.0, float(item.get("unit_cost_cad", item.get("landed_cost_cad", 0.0)) or 0.0)) for item in items)
        return {"units": float(total_units), "asset_value_cad": round(total_cost, 2),
                "average_unit_cost_cad": round(total_cost / max(1, total_units), 4)}
