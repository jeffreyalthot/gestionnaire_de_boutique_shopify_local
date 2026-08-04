class TradeAssuranceVerifier:
    def verify(self,profile: dict[str,object]) -> dict[str,object]:
        enabled=bool(profile.get("trade_assurance"));limit=float(profile.get("assurance_limit",0) or 0);years=float(profile.get("years_on_platform",0) or 0);verified=bool(profile.get("verified_supplier"));issues=[]
        if not enabled:issues.append("trade_assurance_disabled")
        if limit<=0:issues.append("assurance_limit_missing")
        if years<1:issues.append("insufficient_tenure")
        if not verified:issues.append("supplier_not_verified")
        score=.35*enabled+.25*verified+.20*min(1,years/5)+.20*min(1,limit/10000)
        return {"verified":not issues,"score":round(score,4),"issues":tuple(issues),"coverage_limit":limit}
