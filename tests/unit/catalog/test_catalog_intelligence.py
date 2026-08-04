from catalog.discovery.candidate_deduplicator import CandidateDeduplicator
from catalog.discovery.opportunity_detector import OpportunityDetector
from catalog.discovery.product_candidate import ProductCandidate
from catalog.discovery.query_builder import QueryBuilder
from catalog.intelligence.product_ranker import ProductRanker
from catalog.intelligence.profitability_signal import profitability_signal
from catalog.intelligence.seasonality_signal import seasonality_signal
from catalog.intelligence.trend_signal import trend_signal


def candidate(identifier="p1", title="Wireless Lamp"):
    return ProductCandidate(identifier, title, supplier_id="s1", signals={"demand": .9, "margin": .8, "supplier": .9, "quality": .8, "shipping": .7, "competition": .2, "return_risk": .1})


def test_candidate_deduplication():
    items = CandidateDeduplicator().unique([candidate(), candidate(), candidate("p2")])
    assert [item.source_id for item in items] == ["p1", "p2"]


def test_query_builder_removes_stop_words():
    queries = QueryBuilder().build("The lamp for home", include=["LED"])
    assert queries[0] == "lamp home led"
    assert len(queries) == 4


def test_product_ranker_orders_best_first():
    weak = candidate("weak")
    weak.signals = {name: .1 for name in weak.signals}
    ranked = ProductRanker().rank([weak, candidate("strong")])
    assert ranked[0].candidate.source_id == "strong"


def test_opportunity_detector_applies_margin_threshold():
    item = candidate()
    item.signals.update({"competition": .1, "return_risk": .1})
    result = OpportunityDetector().evaluate(item, minimum_margin=.35)
    assert result["accepted"]


def test_signals_are_bounded():
    assert 0 <= trend_signal([1, 2, 3, 4, 5]) <= 1
    assert 0 <= seasonality_signal(12, 12) <= 1
    assert profitability_signal(100, 40) == 1.0
