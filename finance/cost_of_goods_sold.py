from __future__ import annotations


def calculate_cogs(lines: list[dict[str, object]]) -> dict[str, float]:
    product = sum(max(0, int(line.get("quantity", 0) or 0)) * max(0.0, float(line.get("unit_supplier_cost_cad", 0.0) or 0.0)) for line in lines)
    inbound = sum(max(0.0, float(line.get("allocated_shipping_cad", 0.0) or 0.0)) for line in lines)
    duty = sum(max(0.0, float(line.get("allocated_duty_cad", 0.0) or 0.0)) for line in lines)
    return {"product_cad": round(product, 2), "inbound_shipping_cad": round(inbound, 2),
            "duty_cad": round(duty, 2), "total_cad": round(product + inbound + duty, 2)}
