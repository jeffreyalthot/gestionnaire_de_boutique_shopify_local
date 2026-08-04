from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SupplierScore:
    total: float
    quality: float
    delivery: float
    communication: float
    compliance: float
    price: float

    @classmethod
    def calculate(cls,*,quality: float,delivery: float,communication: float,compliance: float,price: float):
        vals=[max(0,min(1,x)) for x in (quality,delivery,communication,compliance,price)]
        total=vals[0]*.30+vals[1]*.25+vals[2]*.15+vals[3]*.20+vals[4]*.10
        return cls(round(total,4),*vals)
