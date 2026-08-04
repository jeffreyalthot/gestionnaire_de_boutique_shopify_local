from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict,dataclass
from decimal import Decimal,ROUND_HALF_UP
from typing import Iterable

@dataclass(frozen=True,slots=True)
class DimensionProfit:
    key: str
    revenue_cad: Decimal
    costs_cad: Decimal
    profit_cad: Decimal
    margin_percent: Decimal
    orders: int
    share_percent: Decimal
    def as_dict(self): return {k:str(v) if isinstance(v,Decimal) else v for k,v in asdict(self).items()}

class ProfitDimensionAnalyzer:
    def analyze(self,items: Iterable[dict[str,object]],dimension: str) -> tuple[DimensionProfit,...]:
        grouped: dict[str,dict[str,object]]=defaultdict(lambda:{"revenue":Decimal("0"),"costs":Decimal("0"),"profit":Decimal("0"),"orders":set()})
        for item in items:
            key=str(item.get(dimension,"unknown")); revenue=Decimal(str(item.get("revenue_cad",item.get("sales_cad",0)) or 0)); profit=Decimal(str(item.get("profit_cad",0) or 0)); costs=Decimal(str(item.get("costs_cad",revenue-profit) or 0))
            row=grouped[key]; row["revenue"]+=revenue; row["profit"]+=profit; row["costs"]+=costs; row["orders"].add(str(item.get("order_id",len(row["orders"]))))
        total_profit=sum((row["profit"] for row in grouped.values()),Decimal("0")); q=Decimal("0.01")
        result=[]
        for key,row in grouped.items():
            revenue=row["revenue"]; profit=row["profit"]
            margin=(profit/revenue*100) if revenue else Decimal("0"); share=(profit/total_profit*100) if total_profit else Decimal("0")
            result.append(DimensionProfit(key,revenue.quantize(q),row["costs"].quantize(q),profit.quantize(q),margin.quantize(q,rounding=ROUND_HALF_UP),len(row["orders"]),share.quantize(q,rounding=ROUND_HALF_UP)))
        return tuple(sorted(result,key=lambda x:(-x.profit_cad,x.key)))

def profit_by(items: Iterable[dict[str,object]],dimension: str) -> dict[str,float]:
    return {row.key:float(row.profit_cad) for row in ProfitDimensionAnalyzer().analyze(items,dimension)}
