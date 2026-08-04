import re


class SupplierIdentityResolver:
    def key(self,name: str,country_code: str,registration_id: str="") -> str:
        clean=re.sub(r"[^a-z0-9]","",name.lower()); return f"{country_code.upper()}:{registration_id or clean}"
