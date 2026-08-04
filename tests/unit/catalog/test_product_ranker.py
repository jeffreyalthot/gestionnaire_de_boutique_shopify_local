from catalog.discovery.product_candidate import ProductCandidate
from catalog.intelligence.product_ranker import ProductRanker

def test_product_ranker_orders_best_candidate_first():
    high=ProductCandidate("h","High",signals={"demand":1,"margin":1,"supplier":1,"quality":1,"shipping":1,"competition":0,"return_risk":0})
    low=ProductCandidate("l","Low",signals={name:0 for name in ProductRanker.WEIGHTS})
    assert ProductRanker().rank([low,high])[0].candidate.source_id=="h"
