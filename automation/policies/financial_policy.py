from automation.policies.rule_policy import RulePolicy


class FinancialPolicy(RulePolicy):
    name = "financial"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.95)
        super().__init__(**kwargs)
