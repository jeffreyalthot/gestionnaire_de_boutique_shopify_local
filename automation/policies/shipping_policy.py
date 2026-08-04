from automation.policies.rule_policy import RulePolicy


class ShippingPolicy(RulePolicy):
    name = "shipping"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.8)
        super().__init__(**kwargs)
