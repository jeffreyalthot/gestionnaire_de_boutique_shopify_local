from decimal import Decimal
def convert(amount: Decimal,rate: Decimal,buffer_percent: Decimal=Decimal("0")) -> Decimal:
    base=Decimal(str(amount))*Decimal(str(rate))
    return base*(Decimal("1")+Decimal(str(buffer_percent))/Decimal("100"))
