from __future__ import annotations

from collections import Counter


def partial_failure_result(successes: list[dict[str, object]], failures: list[dict[str, object]]) -> dict[str, object]:
    status = "partial" if successes and failures else ("success" if successes else "failed")
    reasons = Counter(str(item.get("reason", item.get("error", "unknown"))) for item in failures)
    retryable = [item for item in failures if bool(item.get("retryable", True))]
    compensation = [
        {"action": "cancel_supplier_order", "supplier_order_id": item.get("supplier_order_id", "")}
        for item in successes if item.get("supplier_order_id") and bool(item.get("compensatable", False))
    ]
    return {
        "status": status,
        "successes": [dict(item) for item in successes],
        "failures": [dict(item) for item in failures],
        "failure_reasons": dict(reasons),
        "retryable": retryable,
        "compensation_plan": compensation,
        "success_rate": len(successes) / max(1, len(successes) + len(failures)),
    }
