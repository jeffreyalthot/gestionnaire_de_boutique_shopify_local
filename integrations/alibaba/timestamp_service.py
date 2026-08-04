from datetime import datetime
from zoneinfo import ZoneInfo
def alibaba_timestamp() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d %H:%M:%S")
