from automation.policies.rule_policy import RulePolicy


class CustomerPolicy(RulePolicy):
    name = "customer"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.75)
        super().__init__(**kwargs)
