from integrations.alibaba.client import AlibabaClient
class PaymentRepository:
    def __init__(self,client: AlibabaClient) -> None: self.client=client
    @property
    def resource(self) -> str: return "payment"
