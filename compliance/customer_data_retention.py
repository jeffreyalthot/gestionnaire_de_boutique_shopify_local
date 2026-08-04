from __future__ import annotations

from dataclasses import asdict,dataclass
from security.data_retention import retention_cutoff
from infrastructure.database.engine import Database

@dataclass(frozen=True,slots=True)
class RetentionPurgeResult:
    addresses_redacted: int
    cutoff: str
    category: str
    dry_run: bool
    def as_dict(self):return asdict(self)

class CustomerDataRetention:
    def __init__(self,db: Database) -> None:self.db=db
    def purge_addresses(self,days: int,*,dry_run: bool=False) -> RetentionPurgeResult:
        cutoff=retention_cutoff(days)
        if dry_run:
            count=int(self.db.scalar("SELECT COUNT(*) FROM orders WHERE updated_at<? AND encrypted_shipping_address<>''",(cutoff,),default=0))
        else:
            count=int(self.db.execute("UPDATE orders SET encrypted_shipping_address='' WHERE updated_at<? AND encrypted_shipping_address<>''",(cutoff,)) or 0)
            if count:self.db.insert_audit("privacy.address_retention","system",{"count":count,"cutoff":cutoff})
        return RetentionPurgeResult(count,cutoff,"shipping_address",dry_run)

def purge_expired_addresses(db: Database,days: int) -> int:return CustomerDataRetention(db).purge_addresses(days).addresses_redacted
