from reports.report_base import QueryReport


class ComplianceExceptionReport(QueryReport):
    name = 'compliance_exceptions'
    query = "SELECT category,severity,status,COUNT(*) count FROM automation_exceptions WHERE category LIKE '%compliance%' OR severity IN ('high','critical') GROUP BY category,severity,status"
