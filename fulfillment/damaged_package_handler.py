from __future__ import annotations


class DamagedPackageHandler:
    def plan(self, *, evidence_count: int, salvageable: bool, order_amount_cad: float) -> dict[str,object]:
        if evidence_count<=0: return {"status":"awaiting_evidence","actions":("request_photos",)}
        actions=["open_supplier_dispute","document_damage"]
        actions.append("partial_refund_review" if salvageable else "replace_or_refund_review")
        return {"status":"review_required","actions":tuple(actions),"exposure_cad":round(max(0.0,order_amount_cad),2)}
