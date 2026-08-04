from analytics.scorecards.base import ScorecardBuilder


class WorkflowScorecard(ScorecardBuilder):
    name = "workflow"
    weights = {'success': 0.35, 'latency': 0.15, 'retries': 0.15, 'reconciliation': 0.2, 'resource': 0.15}
    minimums = {'success': 0.9, 'reconciliation': 0.9}
