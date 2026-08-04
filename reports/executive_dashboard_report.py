from reports.report_base import QueryReport


class ExecutiveDashboardReport(QueryReport):
    name = 'executive_dashboard'
    query = 'SELECT financial_status,fulfillment_status,COUNT(*) count,ROUND(SUM(revenue_cad),2) revenue_cad,ROUND(SUM(profit_cad),2) profit_cad FROM orders GROUP BY financial_status,fulfillment_status'
