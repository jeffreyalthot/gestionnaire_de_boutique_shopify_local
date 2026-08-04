from automation.policies.rule_policy import RulePolicy


class BudgetPolicy(RulePolicy):
    name = "budget"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.7)
        super().__init__(**kwargs)
