from ai.agents.base_agent import PolicyAwareAgent


class ProductQualityAgent(PolicyAwareAgent):
    description = 'Évalue la qualité des données produit.'
    positive_signals = ('content_quality', 'media_quality', 'attribute_quality')
    negative_signals = ('return_risk', 'claim_risk')
    hard_block_signals = ('missing_required_data', 'media_rights_missing')

    def prepare_context(self, context):
        value=dict(context); required=list(value.get("required_fields",[]) or []); product=dict(value.get("product",{}) or {})
        missing=[f for f in required if not product.get(f)]; value.setdefault("missing_required_data", bool(missing)); value["missing_fields"]=missing
        value.setdefault("content_quality", max(0.0,1.0-len(missing)/max(len(required),1))); value.setdefault("media_quality", float(value.get("image_score",.5) or .5)); return value

