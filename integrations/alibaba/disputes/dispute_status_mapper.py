STATUS_MAP={'WAIT_SELLER':'supplier_response','WAIT_BUYER':'merchant_response','SUCCESS':'resolved','CLOSED':'closed','PROCESSING':'open'}
def map_dispute_status(value: str)->str:return STATUS_MAP.get(value.upper(),'unknown')
