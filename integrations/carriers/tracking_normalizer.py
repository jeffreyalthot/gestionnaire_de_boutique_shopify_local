import re
def normalize_tracking_number(value: str)->str:return re.sub(r'[^A-Z0-9]','',value.upper())[:80]
def normalize_carrier(value: str)->str:return ' '.join(value.strip().split())[:80]
