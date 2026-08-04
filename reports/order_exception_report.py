from reports.report_base import QueryReport


class OrderExceptionReport(QueryReport):
    name = 'order_exceptions'
    query = "SELECT risk_level,procurement_status,COUNT(*) count,ROUND(SUM(total_amount),2) exposure FROM orders WHERE risk_level IN ('high','critical') OR procurement_status IN ('failed','blocked','retry') GROUP BY risk_level,procurement_status"
