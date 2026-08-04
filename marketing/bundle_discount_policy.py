class BundleDiscountPolicy:
    def discount(self,item_count: int,gross_margin_percent: float) -> float:
        if item_count<2 or gross_margin_percent<25: return 0.
        return min(15.,(item_count-1)*2.5,max(0.,gross_margin_percent-20)/2)
