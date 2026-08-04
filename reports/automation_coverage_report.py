from reports.report_base import QueryReport


class AutomationCoverageReport(QueryReport):
    name = 'automation_coverage'
    query = 'SELECT name,status,COUNT(*) count FROM automation_actions GROUP BY name,status ORDER BY name,status'
