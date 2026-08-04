from __future__ import annotations

import pytest

from ai.models.anomaly_detector import OnlineAnomalyDetector
from ai.models.contextual_bandit import ContextualBandit
from ai.models.model_result import ModelResult


def test_model_result_normalizes_combines_and_enriches():
    first = ModelResult(float("nan"), 2, ("a", "a"), {"x": 1})
    assert first.value == 0 and first.confidence == 1 and first.reasons == ("a",)
    combined = ModelResult.combine([ModelResult(.2, .5, ("x",)), ModelResult(.8, 1, ("y",))], [1, 3])
    assert combined.value == pytest.approx(.65) and combined.confidence == pytest.approx(.875)
    assert combined.with_reason("z").with_metadata(test=True).metadata["test"] is True


def test_anomaly_detector_fits_without_heavy_dependencies():
    detector = OnlineAnomalyDetector(threshold=3, minimum_samples=5)
    detector.partial_fit([[1], [1.1], [.9], [1.05], [.95]])
    assert detector.fitted and not detector.is_anomaly([1.0])
    assessment = detector.assess([100])
    assert assessment.anomalous and assessment.score >= 3
    assert detector.statistics()["dimensions"] == 1


def test_anomaly_detector_rejects_dimension_mismatch():
    detector = OnlineAnomalyDetector(minimum_samples=3)
    detector.partial_fit([[1, 2], [1, 2], [1, 2]])
    with pytest.raises(ValueError, match="dimension"):
        detector.assess([1])


def test_anomaly_detector_does_not_learn_detected_outlier():
    detector = OnlineAnomalyDetector(threshold=2, minimum_samples=3)
    detector.partial_fit([[1], [1], [1]])
    before = detector.statistics()["observations"]
    assert detector.update_and_assess([100]).anomalous
    assert detector.statistics()["observations"] == before


def test_bandit_scores_filters_and_restores():
    bandit = ContextualBandit(["a", "b"], seed=1)
    first = bandit.choose(allowed_actions={"a"})
    assert first == "a"
    bandit.update("a", .8, weight=2)
    snapshot = bandit.snapshot()
    restored = ContextualBandit(["a", "b"])
    restored.restore(snapshot)
    assert restored.snapshot().counts == snapshot.counts
    assert restored.choose(allowed_actions={"b"}) == "b"


def test_bandit_rejects_empty_allowed_actions():
    bandit = ContextualBandit(["a"])
    with pytest.raises(ValueError, match="no_allowed"):
        bandit.choose(allowed_actions=set())
