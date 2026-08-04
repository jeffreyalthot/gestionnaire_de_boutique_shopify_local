from statistics import median


class SupplierResponseTime:
    def summarize(self,hours: list[float]) -> dict[str,float]:
        values=[max(0,x) for x in hours]; return {"count":len(values),"average_hours":round(sum(values)/max(1,len(values)),2),"median_hours":round(median(values),2) if values else 0}
