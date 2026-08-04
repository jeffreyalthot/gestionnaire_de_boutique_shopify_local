from reports.report_base import QueryReport


class CustomerServiceReport(QueryReport):
    name = 'customer_service'
    query = 'SELECT category,status,COUNT(*) count,ROUND(AVG(priority),2) average_priority FROM customer_tickets GROUP BY category,status'
