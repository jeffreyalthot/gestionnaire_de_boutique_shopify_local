class MinimumAdvertisedPricePolicy:
    def enforce(self, proposed_cad: float, minimum_cad: float | None) -> tuple[bool,float,str]:
        if minimum_cad is None: return True,proposed_cad,"not_applicable"
        if proposed_cad<minimum_cad: return False,minimum_cad,"below_map"
        return True,proposed_cad,"allowed"
