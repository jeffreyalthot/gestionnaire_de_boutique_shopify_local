from automation.policies.rule_policy import RulePolicy


class CatalogPolicy(RulePolicy):
    name = "catalog"

    def __init__(self, **kwargs):
        kwargs.setdefault("minimum_score", 0.68)
        super().__init__(**kwargs)
