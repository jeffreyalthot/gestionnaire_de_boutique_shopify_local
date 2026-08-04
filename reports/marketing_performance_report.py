from reports.report_base import QueryReport


class MarketingPerformanceReport(QueryReport):
    name = 'marketing_performance'
    query = "SELECT key,value_json,updated_at FROM key_values WHERE key LIKE 'marketing:%' ORDER BY key"
