from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SampleReview:
    passed: bool
    score: float
    failures: tuple[str,...]
class SampleQualityReview:
    def score(self,checks: dict[str,float]) -> float:return self.review(checks).score
    def review(self,checks: dict[str,float],thresholds: dict[str,float] | None=None,minimum_total: float=.75) -> SampleReview:
        if not checks:return SampleReview(False,0.0,("missing_checks",))
        thresholds=thresholds or {};normalized={k:max(0,min(1,float(v))) for k,v in checks.items()};failures=tuple(k for k,v in normalized.items() if v<float(thresholds.get(k,.65)));score=sum(normalized.values())/len(normalized)
        if score<minimum_total:failures=tuple(dict.fromkeys((*failures,"total_score_below_minimum")))
        return SampleReview(not failures,round(score,4),failures)
