class SupplierQualityHistory:
    def metrics(self,reviews: list[dict[str,object]]) -> dict[str,float]:
        scores=[float(x.get("score",0)) for x in reviews]; defects=sum(bool(x.get("defect")) for x in reviews)
        return {"reviews":len(scores),"average_score":round(sum(scores)/max(1,len(scores)),4),"defect_rate":round(defects/max(1,len(scores)),4)}
