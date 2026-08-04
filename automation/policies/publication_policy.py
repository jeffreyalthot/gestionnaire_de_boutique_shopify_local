from automation.policies.rule_policy import RulePolicy


class PublicationPolicy(RulePolicy):
    name = "publication"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.9)
        super().__init__(**kwargs)
