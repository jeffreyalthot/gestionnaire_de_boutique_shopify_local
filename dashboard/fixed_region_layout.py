from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Region:
    name: str
    start: int
    height: int

    @property
    def end(self) -> int:
        return self.start + self.height - 1


class FixedRegionLayout:
    def __init__(self, line_count: int) -> None:
        if line_count < 8:
            raise ValueError('Un terminal fixe exige au moins huit lignes.')
        self.line_count = line_count
        self._regions: dict[str, Region] = {}

    def reserve(self, name: str, start: int, height: int) -> Region:
        region = Region(name, start, height)
        if start < 0 or height < 1 or region.end >= self.line_count:
            raise ValueError('Région hors écran.')
        if any(not (region.end < existing.start or region.start > existing.end)
               for existing in self._regions.values()):
            raise ValueError('Chevauchement de régions fixes.')
        self._regions[name] = region
        return region

    def regions(self) -> tuple[Region, ...]:
        return tuple(sorted(self._regions.values(), key=lambda item: item.start))
