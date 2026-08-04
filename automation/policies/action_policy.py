from automation.policies.rule_policy import RulePolicy


class ActionPolicyRule(RulePolicy):
    name = "action"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.0)
        super().__init__(**kwargs)
