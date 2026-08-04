from suppliers.supplier_score import SupplierScorer

def test_supplier_score_distinguishes_reliable_supplier():
    scorer=SupplierScorer(); strong=scorer.score("strong",{name:1 for name in scorer.WEIGHTS}); weak=scorer.score("weak",{name:0 for name in scorer.WEIGHTS})
    assert strong.score>weak.score and strong.risk_level=="low" and weak.risk_level=="critical"
