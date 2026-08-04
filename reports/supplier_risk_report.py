from reports.report_base import QueryReport


class SupplierRiskReport(QueryReport):
    name = 'supplier_risk'
    query = "SELECT supplier_id,score,risk_level,metrics_json,updated_at FROM supplier_scores WHERE risk_level IN ('medium','high','critical') OR score<0.65 ORDER BY score ASC"
