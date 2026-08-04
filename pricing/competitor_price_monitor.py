from statistics import median


class CompetitorPriceMonitor:
    def summarize(self, prices_cad: list[float]) -> dict[str,float]:
        values=sorted(x for x in prices_cad if x>0)
        if not values: return {"count":0,"min":0,"median":0,"max":0}
        return {"count":len(values),"min":values[0],"median":round(median(values),2),"max":values[-1]}
