from __future__ import annotations


class UndeliverableHandler:
    def plan(self, *, address_confirmed: bool, return_to_sender: bool, reship_cost_cad: float) -> dict[str,object]:
        if not address_confirmed: return {"status":"customer_action","actions":("request_address_confirmation",)}
        actions=["hold_refund"]
        if return_to_sender: actions.append("monitor_return")
        actions.append("reship_approval" if reship_cost_cad>0 else "reship")
        return {"status":"review_required","actions":tuple(actions),"reship_cost_cad":round(max(0.0,reship_cost_cad),2)}
