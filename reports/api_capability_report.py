from reports.report_base import QueryReport


class ApiCapabilityReport(QueryReport):
    name = 'api_capability'
    query = "SELECT key,value_json,updated_at FROM key_values WHERE key LIKE 'capability:%' ORDER BY key"
