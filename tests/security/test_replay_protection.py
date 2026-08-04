from datetime import datetime,timezone
from security.replay_protection import timestamp_within_window
def test_current_timestamp(): assert timestamp_within_window(datetime.now(timezone.utc))
