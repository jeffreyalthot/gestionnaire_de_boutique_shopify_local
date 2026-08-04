from analytics.scorecards.base import ScorecardBuilder


class SupplierScorecard(ScorecardBuilder):
    name = "supplier"
    weights = {'quality': 0.25, 'delivery': 0.25, 'response': 0.15, 'price': 0.15, 'compliance': 0.2}
    minimums = {'quality': 0.7, 'compliance': 0.85}
