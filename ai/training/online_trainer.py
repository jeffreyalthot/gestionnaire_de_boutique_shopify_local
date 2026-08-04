from __future__ import annotations

from dataclasses import asdict, dataclass
from time import monotonic
from typing import Any, Iterable


@dataclass(frozen=True, slots=True)
class TrainingResult:
    model: str
    samples: int
    batches: int
    elapsed_seconds: float
    status: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class OnlineTrainer:
    def __init__(self, models: dict[str, object], *, batch_size: int = 128) -> None:
        self.models = models
        self.batch_size = max(1, int(batch_size))

    def register(self, name: str, model: object, *, replace: bool = False) -> None:
        if name in self.models and not replace:
            raise ValueError(f"model already registered: {name}")
        self.models[str(name)] = model

    def train_text(self, name: str, texts: list[str], labels: list[str]) -> None:
        self.train(name, texts, labels)

    def train(self, name: str, features: Iterable[Any], labels: Iterable[Any]) -> TrainingResult:
        model = self.models[name]
        x = list(features)
        y = list(labels)
        if len(x) != len(y):
            raise ValueError("features and labels must have the same length")
        if not hasattr(model, "partial_fit"):
            raise TypeError(f"model {name} does not support partial_fit")
        started = monotonic()
        batches = 0
        for offset in range(0, len(x), self.batch_size):
            model.partial_fit(x[offset: offset + self.batch_size], y[offset: offset + self.batch_size])
            batches += 1
        return TrainingResult(name, len(x), batches, monotonic() - started, "trained")

    def predict(self, name: str, features: Iterable[Any]) -> list[Any]:
        model = self.models[name]
        if not hasattr(model, "predict"):
            raise TypeError(f"model {name} does not support predict")
        return list(model.predict(list(features)))

    def snapshot(self) -> dict[str, object]:
        return {
            "models": tuple(sorted(self.models)),
            "batch_size": self.batch_size,
            "trainable": tuple(sorted(name for name, model in self.models.items() if hasattr(model, "partial_fit"))),
        }
