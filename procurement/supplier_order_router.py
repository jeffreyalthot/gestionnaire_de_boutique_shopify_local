from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class SupplierOrderRoute:
    channel: str
    automated: bool
    approval_required: bool
    reason: str

    def as_dict(self) -> dict[str, object]: return asdict(self)


class SupplierOrderRouter:
    def route(self, supplier: dict[str, object]) -> str:
        return self.decide(supplier).channel

    def decide(self, supplier: dict[str, object]) -> SupplierOrderRoute:
        capabilities = set(supplier.get("capabilities", ()) or ())
        if supplier.get("blocked"):
            return SupplierOrderRoute("blocked", False, True, "supplier_blocked")
        if "dropshipping_api" in capabilities:
            return SupplierOrderRoute("dropshipping_api", True, False, "native_dropshipping")
        if "trade_assurance_api" in capabilities:
            return SupplierOrderRoute("trade_assurance_api", True, True, "trade_assurance")
        if "buy_now_api" in capabilities:
            return SupplierOrderRoute("buy_now_api", True, True, "buy_now")
        return SupplierOrderRoute("manual_approval", False, True, "no_supported_order_api")
