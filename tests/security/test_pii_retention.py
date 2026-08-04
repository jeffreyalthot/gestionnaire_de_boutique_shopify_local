from datetime import datetime,timezone
from security.data_retention import retention_cutoff

def test_pii_retention_cutoff_is_in_the_past():
    cutoff=datetime.fromisoformat(retention_cutoff(30))
    assert cutoff < datetime.now(timezone.utc)
