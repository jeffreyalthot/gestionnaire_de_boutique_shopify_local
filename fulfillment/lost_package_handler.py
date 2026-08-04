from __future__ import annotations


class LostPackageHandler:
    def plan(self, *, order_amount_cad: float, insured: bool, carrier_claim_available: bool) -> dict[str,object]:
        actions=["open_supplier_case","notify_customer"]
        if carrier_claim_available: actions.append("open_carrier_claim")
        actions.append("replacement_review" if order_amount_cad>=100 else "refund_or_replace")
        return {"status":"review_required","actions":tuple(actions),"reserve_cad":round(max(0.0,order_amount_cad),2),"insured":insured}
