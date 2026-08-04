class CountryRuleRegistry:
    def __init__(self) -> None:self._rules={}
    def register(self,country: str,rule: dict[str,object]) -> None:self._rules[country.upper()]=dict(rule)
    def get(self,country: str):return self._rules.get(country.upper(),{})
