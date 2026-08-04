from dataclasses import dataclass
from observability.metrics import metrics

@dataclass(slots=True)
class ResourceMetrics:
    prefix: str
    def record(self, name: str, value: float = 1) -> None:
        metrics.inc(f"{self.prefix}.{name}", value)
