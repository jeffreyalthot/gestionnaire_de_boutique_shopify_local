from reports.report_base import QueryReport


class DataQualityReport(QueryReport):
    name = 'data_quality'
    query = 'SELECT status,COUNT(*) count,ROUND(AVG(score),4) average_score FROM products GROUP BY status'
