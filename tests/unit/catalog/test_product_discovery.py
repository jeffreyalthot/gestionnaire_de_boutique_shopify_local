from catalog.discovery.opportunity_detector import OpportunityDetector
from catalog.discovery.product_candidate import ProductCandidate

def test_product_discovery_accepts_strong_opportunity():
    candidate=ProductCandidate("p1","Widget","s1",signals={"demand":.95,"competition":.1,"supplier":.9,"margin":.8,"return_risk":.1})
    result=OpportunityDetector().evaluate(candidate)
    assert result["accepted"] and result["score"]>.68
