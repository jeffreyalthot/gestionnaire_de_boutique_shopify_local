from automation.policies.rule_policy import RulePolicy


class AutonomyModePolicy(RulePolicy):
    name = "autonomy_mode"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.92)
        super().__init__(**kwargs)
