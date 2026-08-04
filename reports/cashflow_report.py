from reports.report_base import QueryReport


class CashflowReport(QueryReport):
    name = 'cashflow'
    query = 'SELECT account,SUM(debit) debit,SUM(credit) credit,currency FROM ledger GROUP BY account,currency ORDER BY account'
