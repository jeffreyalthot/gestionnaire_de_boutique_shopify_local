from analytics.scorecards.base import ScorecardBuilder


class CatalogScorecard(ScorecardBuilder):
    name = "catalog"
    weights = {'coverage': 0.25, 'quality': 0.25, 'freshness': 0.2, 'compliance': 0.2, 'media': 0.1}
    minimums = {'quality': 0.7, 'compliance': 0.9}
