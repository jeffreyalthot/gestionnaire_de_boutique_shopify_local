from __future__ import annotations
from dataclasses import dataclass

_ALWAYS_APPROVE = frozenset({"pay_supplier", "refund", "delete_product", "publish_product", "change_bank_account", "rotate_credentials"})

@dataclass(frozen=True, slots=True)
class ApprovalRequirement:
    required: bool
    action: str
    amount_cad: float
    reason: str

def approval_requirement(action: str, amount_cad: float = 0.0, threshold: float = 0.0, *, irreversible: bool = False, financial: bool = False) -> ApprovalRequirement:
    normalized = action.strip().lower().replace("-", "_")
    amount = max(0.0, float(amount_cad))
    limit = max(0.0, float(threshold))
    if normalized in _ALWAYS_APPROVE:
        return ApprovalRequirement(True, normalized, amount, "Action sensible protégée.")
    if irreversible:
        return ApprovalRequirement(True, normalized, amount, "Action irréversible.")
    if financial and amount > 0:
        return ApprovalRequirement(True, normalized, amount, "Mutation financière.")
    if amount > limit:
        return ApprovalRequirement(True, normalized, amount, f"Montant supérieur au plafond de {limit:.2f} CAD.")
    return ApprovalRequirement(False, normalized, amount, "Action dans les limites autonomes.")

def requires_approval(action: str, amount_cad: float, threshold: float = 0) -> bool:
    return approval_requirement(action, amount_cad, threshold).required
