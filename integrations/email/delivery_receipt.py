from dataclasses import dataclass
from datetime import datetime,timezone
@dataclass(frozen=True)
class DeliveryReceipt:
    message_id: str; recipient: str; status: str; at: str
    @classmethod
    def create(cls,message_id: str,recipient: str,status: str):return cls(message_id,recipient,status,datetime.now(timezone.utc).isoformat())
