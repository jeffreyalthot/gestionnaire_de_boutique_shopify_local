from automation.policies.rule_policy import RulePolicy


class ApprovalPolicy(RulePolicy):
    name = "approval"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 1.0)
        super().__init__(**kwargs)
