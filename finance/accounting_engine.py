from finance.double_entry_ledger import DoubleEntryLedger
class AccountingEngine:
    def __init__(self,ledger: DoubleEntryLedger) -> None: self.ledger=ledger
    def recognize_sale(self,order_id: str,amount: float) -> None:
        self.ledger.post(f"sale:{order_id}","cash_receivable","sales_revenue",amount,memo="Vente Shopify")
    def recognize_supplier_cost(self,order_id: str,amount: float) -> None:
        self.ledger.post(f"cogs:{order_id}","cost_of_goods_sold","cash_payable",amount,memo="Achat Alibaba")
    def recognize_shipping(self,order_id: str,amount: float) -> None:
        self.ledger.post(f"shipping:{order_id}","shipping_expense","cash_payable",amount,memo="Transport fournisseur")
    def recognize_refund(self,order_id: str,amount: float) -> None:
        self.ledger.post(f"refund:{order_id}","sales_returns","cash_receivable",amount,memo="Remboursement client")
