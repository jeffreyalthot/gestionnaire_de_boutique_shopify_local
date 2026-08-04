from __future__ import annotations

import json
from time import monotonic
from uuid import uuid4

from ai.models.product_ranker import product_rank
from ai.models.supplier_risk_model import supplier_risk
from ai.models.text_category_model import TextCategoryModel
from ai.runtime.cpu_budget import CPUBudget
from ai.runtime.fallback_engine import FallbackEngine
from ai.runtime.inference_scheduler import InferenceScheduler
from ai.runtime.memory_budget import MemoryBudget
from ai.runtime.model_registry import ModelRegistry
from ai.runtime.resource_guard import ResourceGuard
from config.settings import Settings
from infrastructure.database.engine import Database, utcnow


class AIRuntime:
    """Low-resource inference runtime with deterministic fallback and telemetry."""

    def __init__(self, settings: Settings, db: Database) -> None:
        self.settings = settings
        self.db = db
        self.memory = MemoryBudget(settings.ai_max_ram_mb)
        self.cpu = CPUBudget(settings.ai_max_cpu_percent)
        self.guard = ResourceGuard(self.memory, self.cpu)
        self.scheduler = InferenceScheduler(settings.ai_worker_threads)
        self.registry = ModelRegistry()
        self.category_model = TextCategoryModel()
        self.fallback = FallbackEngine()
        self.registry.register("category", self.category_model, metadata={"kind": "online_text_classifier"})
        self._started_at = monotonic()
        self._decisions = 0

    def status(self) -> dict[str, object]:
        memory = self.memory.snapshot()
        cpu = self.cpu.snapshot()
        return {
            "enabled": self.settings.ai_enabled,
            "profile": self.settings.ai_profile,
            "rss_mb": memory.rss_mb,
            "limit_mb": memory.limit_mb,
            "available_mb": memory.available_mb,
            "within_budget": memory.within_budget and not cpu.overloaded,
            "cpu": cpu.as_dict(),
            "models": self.registry.names(),
            "model_registry": self.registry.snapshot(),
            "scheduler": self.scheduler.stats().as_dict(),
            "guard": self.guard.stats().as_dict(),
            "decisions": self._decisions,
            "uptime_seconds": round(monotonic() - self._started_at, 3),
        }

    async def score_product(self, features: dict[str, float], entity_id: str = "") -> dict[str, object]:
        if not self.settings.ai_enabled:
            return {"score": 0.5, "confidence": 0.0, "source": "disabled"}
        with self.guard.inference():
            score = await self.scheduler.run(product_rank, features, timeout=15)
        confidence = min(0.99, 0.70 + abs(score - 0.5) * 0.5)
        decision_id = self._record("product_selection", entity_id, confidence, "accept" if score >= 0.7 else "review", features)
        return {"score": score, "confidence": confidence, "source": "deterministic_ranker", "decision_id": decision_id}

    async def score_supplier(self, features: dict[str, float], entity_id: str = "") -> dict[str, object]:
        with self.guard.inference():
            risk = await self.scheduler.run(
                supplier_risk,
                features.get("dispute_rate", 0),
                features.get("response_rate", 0),
                features.get("years", 0),
                bool(features.get("verified", 0)),
                timeout=15,
            )
        confidence = min(.95, .65 + min(1.0, len(features) / 8) * .25)
        decision_id = self._record("supplier_risk", entity_id, confidence, "approve" if risk < 0.3 else "review", features)
        return {"risk": risk, "confidence": confidence, "source": "supplier_risk_model", "decision_id": decision_id}

    def classify_text(self, text: str) -> dict[str, object]:
        if self.settings.ai_enabled:
            try:
                category = self.category_model.predict(text)
                if category:
                    return {"category": category, "confidence": .75, "source": "online_classifier"}
            except Exception:
                pass
        result = self.fallback.classify_with_metadata(text)
        return {**result.as_dict(), "source": "deterministic_fallback"}

    def _record(self, decision_type: str, entity_id: str, confidence: float,
                action: str, features: dict[str, float]) -> str:
        decision_id = str(uuid4())
        self.db.execute(
            "INSERT INTO ai_decisions(id,decision_type,entity_id,confidence,action,features_json,created_at) VALUES(?,?,?,?,?,?,?)",
            (decision_id, decision_type, entity_id, confidence, action,
             json.dumps(features, ensure_ascii=False, sort_keys=True), utcnow()),
        )
        self._decisions += 1
        return decision_id
