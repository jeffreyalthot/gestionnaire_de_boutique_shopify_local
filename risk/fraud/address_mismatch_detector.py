class AddressMismatchDetector:
    def score(self, billing: dict[str,object], shipping: dict[str,object]) -> float:
        keys=("country_code","postal_code","city","last_name")
        mismatches=sum(str(billing.get(k,"")).strip().lower()!=str(shipping.get(k,"")).strip().lower() for k in keys)
        return round(mismatches/len(keys),4)
