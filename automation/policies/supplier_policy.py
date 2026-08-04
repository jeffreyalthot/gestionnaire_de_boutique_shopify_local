from automation.policies.rule_policy import RulePolicy


class SupplierPolicy(RulePolicy):
    name = "supplier"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.65)
        super().__init__(**kwargs)
