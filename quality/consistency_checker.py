from quality.validation_report import ValidationReport


class ConsistencyChecker:
    def check(self,p: dict[str,object]) -> ValidationReport:
        issues=[]
        if float(p.get("price_cad",0) or 0)<float(p.get("landed_cost_cad",0) or 0): issues.append("price_below_cost")
        if int(p.get("stock",0) or 0)<0: issues.append("negative_stock")
        return ValidationReport(not issues,max(0,1-len(issues)*.5),tuple(issues))
