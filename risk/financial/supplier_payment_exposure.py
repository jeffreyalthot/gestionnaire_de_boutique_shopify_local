from risk.risk_score import RiskScore


class SupplierPaymentExposure:
    def assess(self, *, amount_cad: float, supplier_score: float, insured: bool=False) -> RiskScore:
        score=min(1,amount_cad/5000+(1-max(0,min(1,supplier_score)))*.6-(.15 if insured else 0))
        return RiskScore.build(score,("uninsured_supplier_payment",) if not insured and amount_cad>=500 else ())
