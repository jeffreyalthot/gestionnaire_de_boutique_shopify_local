class CurrencyVolatilityBuffer:
    def apply(self, amount_cad: float, annualized_volatility: float, horizon_days: int=30) -> float:
        factor=max(0.0,annualized_volatility)*(max(1,horizon_days)/365)**0.5
        return round(amount_cad*(1+min(0.25,factor)),2)
