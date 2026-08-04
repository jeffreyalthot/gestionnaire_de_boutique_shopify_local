from automation.policies.rule_policy import RulePolicy


class RiskPolicy(RulePolicy):
    name = "risk"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.85)
        super().__init__(**kwargs)
