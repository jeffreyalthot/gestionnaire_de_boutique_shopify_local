from __future__ import annotations


def valid_gtin(value: str) -> bool:
    digits = "".join(ch for ch in value if ch.isdigit())
    if len(digits) not in {8, 12, 13, 14}:
        return False
    body, check = digits[:-1], int(digits[-1])
    total = sum(int(ch) * (3 if (len(body) - index) % 2 else 1) for index, ch in enumerate(body))
    return (10 - total % 10) % 10 == check


class BarcodePolicy:
    def evaluate(self, barcode: str, *, authorized: bool = True) -> dict[str, object]:
        if not barcode:
            return {"allowed": True, "normalized": "", "reason": "absent"}
        normalized = "".join(ch for ch in barcode if ch.isdigit())
        if not authorized:
            return {"allowed": False, "normalized": "", "reason": "brand_authorization_required"}
        return {"allowed": valid_gtin(normalized), "normalized": normalized, "reason": "valid" if valid_gtin(normalized) else "invalid_check_digit"}
