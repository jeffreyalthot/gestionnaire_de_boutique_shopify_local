from __future__ import annotations


class ShippingExceptionClassifier:
    def classify(self, status: str, description: str = "") -> dict[str,str|bool]:
        text=f"{status} {description}".casefold()
        if any(x in text for x in ("customs","douane","clearance")): category="customs_delay"
        elif any(x in text for x in ("address","undeliverable","adresse")): category="address_problem"
        elif any(x in text for x in ("damage","damaged","endommag")): category="damaged"
        elif any(x in text for x in ("lost","missing","perdu")): category="lost"
        elif any(x in text for x in ("weather","storm","météo")): category="weather"
        elif any(x in text for x in ("return","returned","retour")): category="returned"
        else: category="carrier_exception"
        return {"category":category,"customer_action_required":category=="address_problem","supplier_claim":category in {"damaged","lost"}}
