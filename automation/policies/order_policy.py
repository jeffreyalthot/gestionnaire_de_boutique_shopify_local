from automation.policies.rule_policy import RulePolicy


class OrderPolicy(RulePolicy):
    name = "order"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.85)
        super().__init__(**kwargs)
