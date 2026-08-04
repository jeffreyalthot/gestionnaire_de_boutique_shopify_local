from automation.policies.rule_policy import RulePolicy


class MarketingPolicy(RulePolicy):
    name = "marketing"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.75)
        super().__init__(**kwargs)
