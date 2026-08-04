from reports.report_base import QueryReport


class ProductProfitabilityReport(QueryReport):
    name = 'product_profitability'
    query = 'SELECT id,title,category,landed_cost_cad,sale_price_cad,ROUND(sale_price_cad-landed_cost_cad,2) gross_profit_cad,CASE WHEN sale_price_cad>0 THEN ROUND((sale_price_cad-landed_cost_cad)*100.0/sale_price_cad,2) ELSE 0 END gross_margin_percent FROM products ORDER BY gross_profit_cad DESC LIMIT 1000'
