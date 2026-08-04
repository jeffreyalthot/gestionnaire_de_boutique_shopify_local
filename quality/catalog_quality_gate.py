from quality.completeness_checker import CompletenessChecker
from quality.consistency_checker import ConsistencyChecker


class CatalogQualityGate:
    def evaluate(self,p: dict[str,object]):
        a=CompletenessChecker().check(p,("title","description","price_cad","images")); b=ConsistencyChecker().check(p); return {"allowed":a.valid and b.valid and min(a.score,b.score)>=.7,"score":round((a.score+b.score)/2,4),"issues":a.issues+b.issues}
