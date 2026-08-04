ALLOWED_AUTOMATIC={"calculate_price","estimate_profit","reconcile"}
FORBIDDEN_AUTOMATIC={"submit_card_data","change_bank_account"}
def financial_action_allowed(action: str,approved: bool) -> bool:
    if action in FORBIDDEN_AUTOMATIC: return False
    return action in ALLOWED_AUTOMATIC or approved
