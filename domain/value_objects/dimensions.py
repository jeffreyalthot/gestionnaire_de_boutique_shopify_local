from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class Dimensions:
    length_cm: float
    width_cm: float
    height_cm: float
    def volume_cm3(self) -> float:
        return self.length_cm * self.width_cm * self.height_cm
