from __future__ import annotations
class ShopifyGraphqlResponseError(ValueError):pass
class GraphqlResponseValidator:
    def validate(self,payload: dict,root_field: str|None=None)->dict:
        if not isinstance(payload,dict):raise ShopifyGraphqlResponseError('Réponse Shopify invalide.')
        if payload.get('errors'):raise ShopifyGraphqlResponseError('; '.join(str(e.get('message','Erreur')) for e in payload['errors']))
        data=payload.get('data')
        if not isinstance(data,dict):raise ShopifyGraphqlResponseError('Champ data absent.')
        if root_field and root_field not in data:raise ShopifyGraphqlResponseError(f'Champ racine absent: {root_field}')
        return data
