from __future__ import annotations

import re
from hashlib import sha256
from typing import Iterable

from catalog.discovery.product_candidate import ProductCandidate


class CandidateDeduplicator:
    @staticmethod
    def fingerprint(candidate: ProductCandidate) -> str:
        normalized = re.sub(r"[^a-z0-9]+", " ", candidate.title.lower()).strip()
        payload = f"{candidate.source_id}|{candidate.supplier_id}|{normalized}"
        return sha256(payload.encode("utf-8")).hexdigest()

    def unique(self, candidates: Iterable[ProductCandidate]) -> list[ProductCandidate]:
        seen: set[str] = set()
        output: list[ProductCandidate] = []
        for candidate in candidates:
            key = self.fingerprint(candidate)
            if key not in seen:
                seen.add(key)
                output.append(candidate)
        return output
