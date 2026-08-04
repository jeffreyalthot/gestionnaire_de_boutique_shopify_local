from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PriceChange:
    old: float
    new: float
    absolute: float
    percent: float
    material: bool


class PriceChangeDetector:
    def __init__(self, material_percent: float=3.0) -> None: self.material=max(0,material_percent)
    def detect(self, old: float, new: float) -> PriceChange:
        absolute=round(new-old,2); percent=round(absolute/max(0.01,old)*100,2)
        return PriceChange(old,new,absolute,percent,abs(percent)>=self.material)
