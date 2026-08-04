from __future__ import annotations

from math import sqrt
from typing import Iterable


def binary_metrics(labels: list[int], predictions: list[int]) -> dict[str, float]:
    if len(labels) != len(predictions):
        raise ValueError("labels and predictions must have the same length")
    if not labels:
        return {
            "accuracy": 0.0, "precision": 0.0, "recall": 0.0,
            "specificity": 0.0, "f1": 0.0, "mcc": 0.0,
        }
    tp = sum(actual == predicted == 1 for actual, predicted in zip(labels, predictions))
    tn = sum(actual == predicted == 0 for actual, predicted in zip(labels, predictions))
    fp = sum(actual == 0 and predicted == 1 for actual, predicted in zip(labels, predictions))
    fn = sum(actual == 1 and predicted == 0 for actual, predicted in zip(labels, predictions))
    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    specificity = tn / max(1, tn + fp)
    denominator = sqrt(max(0, (tp + fp) * (tp + fn) * (tn + fp) * (tn + fn)))
    return {
        "accuracy": (tp + tn) / len(labels),
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": 2 * precision * recall / max(1e-12, precision + recall),
        "mcc": ((tp * tn) - (fp * fn)) / denominator if denominator else 0.0,
    }


def regression_metrics(actual: Iterable[float], predicted: Iterable[float]) -> dict[str, float]:
    y = [float(value) for value in actual]
    p = [float(value) for value in predicted]
    if len(y) != len(p):
        raise ValueError("actual and predicted must have the same length")
    if not y:
        return {"mae": 0.0, "rmse": 0.0, "mape": 0.0, "bias": 0.0}
    errors = [prediction - target for target, prediction in zip(y, p)]
    absolute = [abs(value) for value in errors]
    squared = [value * value for value in errors]
    percentage = [abs(error) / abs(target) for target, error in zip(y, errors) if abs(target) > 1e-12]
    return {
        "mae": sum(absolute) / len(absolute),
        "rmse": sqrt(sum(squared) / len(squared)),
        "mape": sum(percentage) / len(percentage) if percentage else 0.0,
        "bias": sum(errors) / len(errors),
    }


def calibration_error(labels: Iterable[int], probabilities: Iterable[float], bins: int = 10) -> float:
    pairs = [(int(label), max(0.0, min(1.0, float(prob)))) for label, prob in zip(labels, probabilities)]
    if not pairs:
        return 0.0
    total = len(pairs)
    error = 0.0
    for index in range(max(1, int(bins))):
        lower = index / bins
        upper = (index + 1) / bins
        bucket = [(label, prob) for label, prob in pairs if lower <= prob < upper or (index == bins - 1 and prob == 1.0)]
        if not bucket:
            continue
        confidence = sum(prob for _, prob in bucket) / len(bucket)
        accuracy = sum(label for label, _ in bucket) / len(bucket)
        error += len(bucket) / total * abs(confidence - accuracy)
    return error
