from pricing.profit_floor_guard import ProfitFloorGuard
class FinancialQualityGate(ProfitFloorGuard):
    def evaluate(self,price_cad: float,landed_cost_cad: float,fees_cad: float=0,minimum_profit_cad: float=1,minimum_margin: float=.15) -> dict[str,object]:
        price=float(price_cad);cost=float(landed_cost_cad)+float(fees_cad);profit=price-cost;margin=profit/max(.01,price);issues=[]
        if profit<minimum_profit_cad:issues.append("profit_below_floor")
        if margin<minimum_margin:issues.append("margin_below_floor")
        if price<=0 or cost<0:issues.append("invalid_amount")
        return {"allowed":not issues,"price_cad":round(price,2),"cost_cad":round(cost,2),"profit_cad":round(profit,2),"margin":round(margin,6),"issues":tuple(issues)}
