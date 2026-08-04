from marketing.seo_auditor import SEOAuditor

def test_seo_auditor_flags_incomplete_product():
    bad=SEOAuditor().audit({"title":"x","description":"short","handle":"","alt_texts":[]})
    good=SEOAuditor().audit({"title":"Excellent product title for Canadian customers","description":"A"*180,"handle":"excellent-product","alt_texts":["front"]})
    assert bad["score"]<good["score"] and good["passed"]
