from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InventoryDrift:
    sku: str
    expected: int
    observed: int
    difference: int
    material: bool


class InventoryDriftDetector:
    def __init__(self, tolerance: int=1) -> None: self.tolerance=max(0,tolerance)
    def detect(self, sku: str, expected: int, observed: int) -> InventoryDrift:
        diff=observed-expected
        return InventoryDrift(sku,expected,observed,diff,abs(diff)>self.tolerance)
