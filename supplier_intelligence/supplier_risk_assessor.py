from __future__ import annotations
from risk.risk_score import RiskScore

class SupplierRiskAssessor:
    def assess(self,p: dict[str,object]) -> RiskScore:
        score=0.;reasons=[];factors={}
        def add(name: str,value: float,reason: str):
            nonlocal score
            if value:score+=value;factors[name]=value;reasons.append(reason)
        if not p.get("verified"):add("unverified",.25,"unverified")
        if not p.get("trade_assurance"):add("trade_assurance",.2,"no_trade_assurance")
        years=float(p.get("years_active",0) or 0)
        if years<1:add("tenure",.15,"new_supplier")
        dispute=max(0,float(p.get("dispute_rate",0) or 0));late=max(0,float(p.get("late_rate",0) or 0));defect=max(0,float(p.get("defect_rate",0) or 0));response=max(0,float(p.get("response_hours",0) or 0))
        add("dispute_rate",min(.25,dispute*2),"high_dispute_rate" if dispute>.03 else "disputes") if dispute else None
        add("late_rate",min(.2,late),"late_delivery") if late else None
        add("defect_rate",min(.25,defect*1.5),"quality_defects") if defect else None
        add("response_time",min(.1,response/1000),"slow_response") if response>48 else None
        if p.get("blacklisted"):add("blacklist",1.,"blacklisted")
        confidence=min(1,.5+len(factors)*.08)
        return RiskScore.build(score,reasons,factors=factors,confidence=confidence)
