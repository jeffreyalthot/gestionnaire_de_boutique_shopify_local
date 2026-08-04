from __future__ import annotations

from ai.features.base import age_hours, as_float, bounded, safe_ratio


def customer_features(customer: dict[str, object]) -> dict[str, float]:
    orders = max(0.0, as_float(customer.get("orders_count")))
    spent = max(0.0, as_float(customer.get("total_spent")))
    refunds = max(0.0, as_float(customer.get("refund_count")))
    chargebacks = max(0.0, as_float(customer.get("chargeback_count")))
    return {
        "orders": orders,
        "spent": spent,
        "average_order_value": safe_ratio(spent, orders),
        "refund_rate": bounded(customer.get("refund_rate", safe_ratio(refunds, orders))),
        "chargeback_rate": bounded(safe_ratio(chargebacks, orders)),
        "account_age_hours": age_hours(customer.get("created_at")),
        "email_verified": float(bool(customer.get("email_verified"))),
        "phone_verified": float(bool(customer.get("phone_verified"))),
        "accepts_marketing": float(bool(customer.get("accepts_marketing"))),
        "lifetime_value": max(0.0, as_float(customer.get("lifetime_value", spent))),
    }
