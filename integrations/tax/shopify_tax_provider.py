from integrations.tax.tax_provider import TaxProvider,TaxQuote
class ShopifyTaxProvider(TaxProvider):
    def __init__(self,calculator)->None:self.calculator=calculator
    async def quote(self,subtotal: float,country: str,province: str='',currency: str='CAD')->TaxQuote:
        value=self.calculator(subtotal=subtotal,country=country,province=province,currency=currency)
        if hasattr(value,'__await__'):value=await value
        tax=round(float(value.get('tax',0)),2);return TaxQuote(subtotal,tax,round(subtotal+tax,2),currency,'shopify')
