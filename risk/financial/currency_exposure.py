from risk.risk_score import RiskScore


class CurrencyExposure:
    def assess(self, *, foreign_amount: float, portfolio_cad: float, volatility: float) -> RiskScore:
        concentration=foreign_amount/max(.01,portfolio_cad); score=min(1,concentration*.6+max(0,volatility)*.8)
        return RiskScore.build(score,("currency_concentration",) if concentration>.25 else ())
