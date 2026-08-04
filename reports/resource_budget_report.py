from reports.report_base import QueryReport


class ResourceBudgetReport(QueryReport):
    name = 'resource_budget'
    query = 'SELECT snapshot_json,created_at FROM runtime_snapshots ORDER BY created_at DESC LIMIT 100'
