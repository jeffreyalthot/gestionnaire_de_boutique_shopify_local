from __future__ import annotations

from compliance.base import ComplianceFinding, result


class BatteryShippingFilter:
    def evaluate(self, product: dict[str, object]):
        battery_type = str(product.get("battery_type", "")).casefold()
        included = bool(product.get("battery_included", False))
        watt_hours = float(product.get("battery_watt_hours", 0.0) or 0.0)
        findings = []
        if included and not battery_type:
            findings.append(ComplianceFinding("battery_type_missing", "error", "Type de batterie requis.", True))
        if battery_type in {"lithium ion", "lithium metal", "li-ion", "lipo"}:
            findings.append(ComplianceFinding("lithium_shipping_review", "warning", "Validation transport batterie requise.", False,
                                               {"battery_type": battery_type, "watt_hours": watt_hours}))
        if watt_hours < 0 or watt_hours > 1000:
            findings.append(ComplianceFinding("battery_capacity_invalid", "error", "Capacité de batterie incohérente.", True))
        return result(*findings)
