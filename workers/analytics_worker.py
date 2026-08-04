from workers.specialized_worker import SpecializedWorker


class AnalyticsWorker(SpecializedWorker):
    name = 'analytics'
    queue = 'analytics'
    accepted_task_types = ('analytics_snapshot', 'forecast_refresh', 'scorecard_refresh')
