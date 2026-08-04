from __future__ import annotations

from collections import defaultdict, deque
from math import ceil
from threading import RLock

from observability.metric_snapshot import MetricSnapshot


class MetricRegistry:
    def __init__(self, *, histogram_samples: int = 512) -> None:
        self._values: dict[str, float] = {}
        self._types: dict[str, str] = {}
        self._labels: dict[str, dict[str, str]] = {}
        self._histograms: dict[str, deque[float]] = defaultdict(lambda: deque(maxlen=max(8, histogram_samples)))
        self._lock = RLock()

    def set(self, name: str, value: float, *, labels: dict[str, str] | None = None) -> None:
        with self._lock:
            self._values[name] = float(value); self._types[name] = "gauge"
            if labels: self._labels[name] = dict(labels)

    def increment(self, name: str, amount: float = 1, *, labels: dict[str, str] | None = None) -> float:
        with self._lock:
            self._values[name] = self._values.get(name, 0) + float(amount); self._types[name] = "counter"
            if labels: self._labels[name] = dict(labels)
            return self._values[name]

    def observe(self, name: str, value: float, *, labels: dict[str, str] | None = None) -> None:
        with self._lock:
            self._histograms[name].append(float(value)); self._types[name] = "histogram"
            if labels: self._labels[name] = dict(labels)
            self._recompute_histogram(name)

    def remove(self, name: str) -> bool:
        with self._lock:
            existed = name in self._values or name in self._histograms
            self._values.pop(name, None); self._types.pop(name, None); self._labels.pop(name, None); self._histograms.pop(name, None)
            return existed

    def snapshot(self, *, prefix: str = "") -> MetricSnapshot:
        with self._lock:
            values = {name: value for name, value in self._values.items() if not prefix or name.startswith(prefix)}
            return MetricSnapshot(values, types={name: self._types.get(name, "gauge") for name in values}, labels={name: dict(self._labels.get(name, {})) for name in values})

    def _recompute_histogram(self, name: str) -> None:
        values = sorted(self._histograms[name])
        if not values: return
        self._values[f"{name}.count"] = float(len(values)); self._values[f"{name}.sum"] = float(sum(values))
        for percentile in (.5, .9, .95, .99):
            index = min(len(values) - 1, max(0, ceil(len(values) * percentile) - 1))
            key = f"{name}.p{int(percentile * 100)}"; self._values[key] = values[index]; self._types[key] = "histogram_quantile"
