from analytics.scorecards.base import ScorecardBuilder


class ProductScorecard(ScorecardBuilder):
    name = "product"
    weights = {'quality': 0.25, 'margin': 0.25, 'demand': 0.2, 'supplier': 0.15, 'return_risk': 0.15}
    minimums = {'quality': 0.7, 'margin': 0.6}
