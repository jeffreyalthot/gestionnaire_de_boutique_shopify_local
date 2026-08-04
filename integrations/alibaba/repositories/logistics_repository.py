from integrations.alibaba.client import AlibabaClient
class LogisticsRepository:
    def __init__(self,client: AlibabaClient) -> None: self.client=client
    @property
    def resource(self) -> str: return "logistics"
