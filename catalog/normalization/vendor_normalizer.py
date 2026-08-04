from __future__ import annotations

import re


class VendorNormalizer:
    def normalize(self, supplier_name: str, *, expose_supplier: bool = False, store_vendor: str = "ELIT21") -> str:
        if not expose_supplier:
            return store_vendor[:100]
        clean = re.sub(r"[^\w .&'-]+", "", " ".join(supplier_name.split()))
        return clean[:100] or store_vendor[:100]
