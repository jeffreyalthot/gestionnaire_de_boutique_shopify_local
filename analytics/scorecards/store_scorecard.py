from analytics.scorecards.base import ScorecardBuilder


class StoreScorecard(ScorecardBuilder):
    name = "store"
    weights = {'profitability': 0.25, 'fulfillment': 0.2, 'customer': 0.2, 'compliance': 0.2, 'reliability': 0.15}
    minimums = {'compliance': 0.9, 'reliability': 0.8}
