from __future__ import annotations

from dataclasses import asdict, dataclass

from returns.return_request import ReturnRequest


@dataclass(frozen=True, slots=True)
class ReturnValidationResult:
    valid: bool
    issues: tuple[str, ...]
    warnings: tuple[str, ...]
    total_quantity: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class ReturnValidator:
    def validate(self, r: ReturnRequest) -> tuple[bool, tuple[str, ...]]:
        result = self.assess(r)
        return result.valid, result.issues

    def assess(self, r: ReturnRequest) -> ReturnValidationResult:
        issues: list[str] = []
        warnings: list[str] = []
        if not str(r.order_id).strip():
            issues.append("missing_order_id")
        if not str(r.reason).strip():
            issues.append("missing_reason")
        if not r.items:
            issues.append("missing_items")
        total = 0
        seen: set[str] = set()
        for item in r.items or ():
            sku = str(item.get("sku") or item.get("line_item_id") or "").strip()
            quantity = int(item.get("quantity", 0) or 0)
            if not sku:
                issues.append("missing_item_identifier")
            if quantity <= 0:
                issues.append("invalid_item_quantity")
            total += max(0, quantity)
            if sku in seen:
                warnings.append("duplicate_item")
            seen.add(sku)
        if total > 100:
            warnings.append("large_return")
        return ReturnValidationResult(not issues, tuple(dict.fromkeys(issues)), tuple(dict.fromkeys(warnings)), total)
