from reports.report_base import QueryReport


class ProductOpportunityReport(QueryReport):
    name = 'product_opportunities'
    query = "SELECT id,title,category,score,landed_cost_cad,sale_price_cad,stock,status FROM products WHERE status IN ('candidate','draft') ORDER BY score DESC,sale_price_cad-landed_cost_cad DESC LIMIT 500"
