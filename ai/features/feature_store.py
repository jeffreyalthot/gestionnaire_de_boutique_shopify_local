from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite
from threading import RLock
from typing import Any, Iterable, Mapping

from infrastructure.database.engine import Database


@dataclass(frozen=True, slots=True)
class FeatureSnapshot:
    entity: str
    entity_id: str
    features: dict[str, float]
    version: int
    updated_at: str
    fingerprint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "entity": self.entity,
            "entity_id": self.entity_id,
            "features": dict(self.features),
            "version": self.version,
            "updated_at": self.updated_at,
            "fingerprint": self.fingerprint,
        }


class FeatureStore:
    """Feature store compact utilisant la base clé-valeur canonique.

    Les méthodes historiques ``set`` et ``get`` sont conservées. Les nouvelles
    méthodes ajoutent version, empreinte, mise à jour partielle et opérations
    par lot sans exiger une base de données supplémentaire.
    """

    def __init__(self, db: Database, *, max_features: int = 512) -> None:
        self.db = db
        self.max_features = max(1, int(max_features))
        self._lock = RLock()
        self.reads = 0
        self.writes = 0
        self.rejected = 0

    @staticmethod
    def _identifier(value: str, label: str) -> str:
        normalized = str(value).strip()
        if not normalized or len(normalized) > 160 or any(ch in normalized for ch in "\r\n\0"):
            raise ValueError(f"{label}_invalid")
        return normalized

    @staticmethod
    def _normalize_features(features: Mapping[str, Any], limit: int) -> dict[str, float]:
        if len(features) > limit:
            raise ValueError("feature_limit_exceeded")
        normalized: dict[str, float] = {}
        for raw_name, raw_value in features.items():
            name = str(raw_name).strip()
            if not name or len(name) > 160 or any(ch in name for ch in "\r\n\0"):
                raise ValueError("feature_name_invalid")
            try:
                number = float(raw_value)
            except (TypeError, ValueError) as exc:
                raise ValueError(f"feature_value_invalid:{name}") from exc
            if not isfinite(number):
                raise ValueError(f"feature_value_non_finite:{name}")
            normalized[name] = number
        return dict(sorted(normalized.items()))

    @staticmethod
    def _key(entity: str, entity_id: str) -> str:
        return f"features:{entity}:{entity_id}"

    @staticmethod
    def _fingerprint(features: Mapping[str, float]) -> str:
        body = json.dumps(features, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return hashlib.sha256(body.encode("utf-8")).hexdigest()

    def snapshot(self, entity: str, entity_id: str) -> FeatureSnapshot | None:
        entity = self._identifier(entity, "entity")
        entity_id = self._identifier(entity_id, "entity_id")
        raw = self.db.get_value(self._key(entity, entity_id), None)
        self.reads += 1
        if raw is None:
            return None
        if isinstance(raw, Mapping) and "features" in raw:
            features = self._normalize_features(dict(raw.get("features", {})), self.max_features)
            version = max(1, int(raw.get("version", 1)))
            updated_at = str(raw.get("updated_at") or "")
            fingerprint = str(raw.get("fingerprint") or self._fingerprint(features))
        else:  # format historique: dictionnaire brut de caractéristiques
            features = self._normalize_features(dict(raw), self.max_features)
            version = 1
            updated_at = ""
            fingerprint = self._fingerprint(features)
        return FeatureSnapshot(entity, entity_id, features, version, updated_at, fingerprint)

    def set(self, entity: str, entity_id: str, features: dict[str, float]) -> None:
        self.put(entity, entity_id, features)

    def put(
        self,
        entity: str,
        entity_id: str,
        features: Mapping[str, Any],
        *,
        expected_version: int | None = None,
        merge: bool = False,
    ) -> FeatureSnapshot:
        entity = self._identifier(entity, "entity")
        entity_id = self._identifier(entity_id, "entity_id")
        incoming = self._normalize_features(features, self.max_features)
        with self._lock:
            previous = self.snapshot(entity, entity_id)
            current_version = previous.version if previous else 0
            if expected_version is not None and int(expected_version) != current_version:
                self.rejected += 1
                raise RuntimeError("feature_version_conflict")
            combined = dict(previous.features) if merge and previous else {}
            combined.update(incoming)
            combined = self._normalize_features(combined, self.max_features)
            snapshot = FeatureSnapshot(
                entity=entity,
                entity_id=entity_id,
                features=combined,
                version=current_version + 1,
                updated_at=datetime.now(timezone.utc).isoformat(),
                fingerprint=self._fingerprint(combined),
            )
            self.db.set_value(self._key(entity, entity_id), snapshot.as_dict())
            self.writes += 1
            return snapshot

    def get(self, entity: str, entity_id: str) -> dict[str, float]:
        snapshot = self.snapshot(entity, entity_id)
        return dict(snapshot.features) if snapshot else {}

    def get_many(self, entity: str, entity_ids: Iterable[str]) -> dict[str, dict[str, float]]:
        return {entity_id: self.get(entity, entity_id) for entity_id in entity_ids}

    def set_many(self, entity: str, records: Mapping[str, Mapping[str, Any]]) -> tuple[FeatureSnapshot, ...]:
        results: list[FeatureSnapshot] = []
        for entity_id, features in records.items():
            results.append(self.put(entity, entity_id, features))
        return tuple(results)

    def delete(self, entity: str, entity_id: str) -> bool:
        entity = self._identifier(entity, "entity")
        entity_id = self._identifier(entity_id, "entity_id")
        key = self._key(entity, entity_id)
        existed = self.db.get_value(key, None) is not None
        if existed:
            # Database n'expose pas encore delete_value; un marqueur nul conserve
            # la compatibilité tout en rendant la lecture équivalente à l'absence.
            self.db.set_value(key, None)
            self.writes += 1
        return existed

    def statistics(self) -> dict[str, int]:
        return {"reads": self.reads, "writes": self.writes, "rejected": self.rejected, "max_features": self.max_features}
