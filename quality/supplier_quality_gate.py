class SupplierQualityGate:
    def evaluate(self,score: float,minimum: float=.65,*,blocked: bool=False,critical_issues: tuple[str,...]=()) -> tuple[bool,str]:
        if blocked:return False,"supplier_blocked"
        if critical_issues:return False,"critical_quality_issue:"+critical_issues[0]
        return (float(score)>=float(minimum),"allowed" if float(score)>=float(minimum) else "supplier_score_below_minimum")
    def report(self,**kwargs) -> dict[str,object]:
        allowed,reason=self.evaluate(**kwargs);return {"allowed":allowed,"reason":reason,"minimum":kwargs.get("minimum",.65),"score":kwargs.get("score",0)}
