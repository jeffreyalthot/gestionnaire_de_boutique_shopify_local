from automation.policies.rule_policy import RulePolicy


class ProcurementPolicy(RulePolicy):
    name = "procurement"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.9)
        super().__init__(**kwargs)
