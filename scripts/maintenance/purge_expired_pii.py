from datetime import datetime,timedelta,timezone
from config.settings import get_settings
from infrastructure.database.engine import Database

settings=get_settings(); db=Database(settings.database_path); db.initialize()
cutoff=(datetime.now(timezone.utc)-timedelta(days=settings.customer_address_retention_days)).isoformat()
count=db.execute("UPDATE orders SET encrypted_shipping_address='' WHERE encrypted_shipping_address<>'' AND created_at<?",(cutoff,))
db.insert_audit("pii_retention_purge","maintenance",{"addresses_redacted":count,"cutoff":cutoff})
print({"addresses_redacted":count})
