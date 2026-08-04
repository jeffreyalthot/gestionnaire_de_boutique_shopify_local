from ai.agents.base_agent import PolicyAwareAgent


class ProductScoutAgent(PolicyAwareAgent):
    description = 'Classe les produits selon potentiel, stock et marge.'
    positive_signals = ('demand_score', 'margin_score', 'supplier_score', 'quality_score')
    negative_signals = ('saturation_score', 'return_risk')
    hard_block_signals = ('restricted_product', 'supplier_blocked')

    def prepare_context(self, context):
        value=dict(context); sales=float(value.get("estimated_monthly_sales",0) or 0); competition=float(value.get("competitor_count",0) or 0)
        value.setdefault("demand_score", min(1.0,sales/100.0)); value.setdefault("saturation_score", min(1.0,competition/100.0))
        value.setdefault("margin_score", float(value.get("gross_margin",.0) or 0)/.5 if float(value.get("gross_margin",0) or 0)>0 else 0.0); return value

