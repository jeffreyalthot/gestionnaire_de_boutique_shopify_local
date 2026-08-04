from __future__ import annotations

from security.pci_guard import reject_payment_card_data

__all__ = ["reject_payment_card_data", "payment_data_scan"]


def payment_data_scan(payload: object) -> dict[str, object]:
    try:
        reject_payment_card_data(payload)
    except ValueError as exc:
        return {"safe": False, "reason": str(exc)}
    return {"safe": True, "reason": "no_forbidden_payment_fields"}
