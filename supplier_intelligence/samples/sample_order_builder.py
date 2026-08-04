from hashlib import sha256
class SampleOrderBuilder:
    def build(self,sku: str,supplier_id: str,quantity: int=1,checks: tuple[str,...]=("dimensions","materials","function","packaging")) -> dict[str,object]:
        sku=sku.strip();supplier_id=supplier_id.strip();quantity=max(1,min(int(quantity),5))
        if not sku or not supplier_id:raise ValueError("sku et fournisseur requis")
        key=sha256(f"{sku}|{supplier_id}|{quantity}|{','.join(checks)}".encode()).hexdigest()
        return {"sku":sku,"supplier_id":supplier_id,"quantity":quantity,"purpose":"quality_validation","required_checks":tuple(dict.fromkeys(checks)),"idempotency_key":key,"status":"planned"}
