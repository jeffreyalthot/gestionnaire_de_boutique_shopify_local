from catalog.discovery.candidate_deduplicator import CandidateDeduplicator
from catalog.discovery.product_candidate import ProductCandidate
from catalog.intelligence.product_ranker import ProductRanker

def test_catalog_candidates_are_deduplicated_and_ranked():
    a=ProductCandidate("p1","Widget","s1",signals={"demand":.9,"margin":.8,"supplier":.9})
    b=ProductCandidate("p1","Widget","s1",signals={"demand":.1})
    unique=CandidateDeduplicator().unique([a,b]); ranked=ProductRanker().rank(unique)
    assert len(unique)==1 and ranked[0].candidate.source_id=="p1"
