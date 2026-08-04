from reports.report_base import QueryReport


class SupplierPerformanceReport(QueryReport):
    name = 'supplier_performance'
    query = 'SELECT supplier_id,score,risk_level,metrics_json,updated_at FROM supplier_scores ORDER BY score DESC'
