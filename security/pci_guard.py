FORBIDDEN_KEYS = {"card_number", "credit_card", "cvv", "cvc", "pin", "track_data"}

def reject_payment_card_data(payload: object) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key.lower() in FORBIDDEN_KEYS:
                raise ValueError(f"Stockage de donnée bancaire interdit: {key}")
            reject_payment_card_data(value)
    elif isinstance(payload, list):
        for item in payload:
            reject_payment_card_data(item)
