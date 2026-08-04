from __future__ import annotations

from dataclasses import asdict, dataclass

from supplier_intelligence.supplier_score import SupplierScore


@dataclass(frozen=True, slots=True)
class RankedSupplier:
    rank: int
    supplier_id: str
    score: SupplierScore
    selected: bool
    gap_to_leader: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class SupplierRanker:
    def rank(self, scores: dict[str, SupplierScore]) -> tuple[tuple[str, SupplierScore], ...]:
        return tuple((item.supplier_id, item.score) for item in self.detailed(scores))

    def detailed(self, scores: dict[str, SupplierScore], *, minimum_total: float = 0, limit: int | None = None) -> tuple[RankedSupplier, ...]:
        ordered = sorted(((supplier_id, score) for supplier_id, score in scores.items() if float(score.total) >= minimum_total), key=lambda item: (-float(item[1].total), item[0]))
        if limit is not None:
            ordered = ordered[:max(0, int(limit))]
        leader = float(ordered[0][1].total) if ordered else 0.0
        return tuple(RankedSupplier(index + 1, supplier_id, score, index == 0, round(leader - float(score.total), 4)) for index, (supplier_id, score) in enumerate(ordered))
