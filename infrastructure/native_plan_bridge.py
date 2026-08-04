from __future__ import annotations

import hashlib
import hmac
import math
import re
from dataclasses import dataclass
from pathlib import Path

from infrastructure.database.engine import Database

_PLAN_ID = re.compile(r"^[0-9a-f]{32}$")
_ACTION = re.compile(r"^[a-z0-9-]{1,64}$")
_ALLOWED_RISKS = {"read-only", "reversible", "irreversible", "financial"}
_EXPECTED_KEYS = (
    "version",
    "id",
    "action",
    "risk",
    "simulated",
    "approved",
    "amount_cad",
    "created_at_utc",
    "checksum",
)


@dataclass(frozen=True, slots=True)
class NativePlan:
    plan_id: str
    action: str
    risk: str
    simulated: bool
    approved: bool
    amount_cad: float
    created_at_utc: str
    checksum: str


class NativePlanBridge:
    def __init__(self, database: Database, root: Path) -> None:
        self.database = database
        self.root = Path(root)
        self.pending = self.root / "pending"
        self.processed = self.root / "processed"
        self.awaiting_approval = self.root / "awaiting_approval"
        self.rejected = self.root / "rejected"
        for directory in (self.pending, self.processed, self.awaiting_approval, self.rejected):
            directory.mkdir(parents=True, exist_ok=True)

    def ingest_pending(self, maximum: int = 64) -> dict[str, int]:
        limit = max(1, min(int(maximum), 64))
        stats = {"scanned": 0, "imported": 0, "duplicates": 0, "awaiting_approval": 0, "rejected": 0}
        candidates = sorted(self.pending.glob("*.plan"), key=lambda path: path.name)[:limit]
        for path in candidates:
            stats["scanned"] += 1
            try:
                if path.is_symlink() or not path.is_file():
                    raise ValueError("plan path is not a regular file")
                plan = self._read_plan(path)
                inserted = self.database.register_native_plan(
                    plan_id=plan.plan_id,
                    action=plan.action,
                    risk=plan.risk,
                    simulated=plan.simulated,
                    approved=plan.approved,
                    amount_cad=plan.amount_cad,
                    source_path=path.name,
                    payload={
                        "created_at_utc": plan.created_at_utc,
                        "checksum": plan.checksum,
                    },
                )
                if not inserted:
                    stats["duplicates"] += 1
                    self._move(path, self.processed)
                    continue

                detail = {
                    "plan_id": plan.plan_id,
                    "action": plan.action,
                    "risk": plan.risk,
                    "simulated": plan.simulated,
                    "approved_in_terminal": plan.approved,
                    "amount_cad": plan.amount_cad,
                    "checksum": plan.checksum,
                }
                self.database.insert_audit("native_plan_ingested", "native-terminal", detail)

                requires_runtime_approval = not plan.simulated and plan.risk in {"irreversible", "financial"}
                if requires_runtime_approval:
                    self.database.request_native_plan_approval(
                        plan.plan_id,
                        plan.action,
                        plan.amount_cad,
                    )
                    self.database.set_native_plan_status(plan.plan_id, "awaiting_approval")
                    self._move(path, self.awaiting_approval)
                    stats["awaiting_approval"] += 1
                else:
                    self.database.set_native_plan_status(plan.plan_id, "imported")
                    self._move(path, self.processed)
                    stats["imported"] += 1
            except (OSError, UnicodeError, ValueError) as error:
                self._reject(path, str(error))
                stats["rejected"] += 1
        return stats

    @staticmethod
    def _read_plan(path: Path) -> NativePlan:
        if path.stat().st_size > 8192:
            raise ValueError("plan exceeds 8192-byte limit")
        raw = path.read_bytes()
        try:
            text = raw.decode("ascii")
        except UnicodeDecodeError as error:
            raise ValueError("plan is not strict ASCII") from error
        if not text.endswith("\n"):
            raise ValueError("plan is not newline terminated")

        lines = text.splitlines(keepends=True)
        if len(lines) != len(_EXPECTED_KEYS):
            raise ValueError("plan field count is invalid")
        values: dict[str, str] = {}
        canonical_parts: list[str] = []
        for index, line in enumerate(lines):
            if not line.endswith("\n") or "=" not in line:
                raise ValueError("plan line format is invalid")
            key, value = line[:-1].split("=", 1)
            if key != _EXPECTED_KEYS[index] or key in values:
                raise ValueError("plan fields are missing, duplicated, or out of order")
            values[key] = value
            if key != "checksum":
                canonical_parts.append(line)

        if values["version"] != "1":
            raise ValueError("unsupported plan version")
        if not _PLAN_ID.fullmatch(values["id"]) or path.name != f"{values['id']}.plan":
            raise ValueError("plan identifier or filename is invalid")
        if not _ACTION.fullmatch(values["action"]):
            raise ValueError("action name is invalid")
        if values["risk"] not in _ALLOWED_RISKS:
            raise ValueError("risk classification is invalid")
        if values["simulated"] not in {"0", "1"} or values["approved"] not in {"0", "1"}:
            raise ValueError("boolean field is invalid")
        if not values["created_at_utc"].endswith("Z") or len(values["created_at_utc"]) != 20:
            raise ValueError("UTC timestamp is invalid")

        try:
            amount = float(values["amount_cad"])
        except ValueError as error:
            raise ValueError("amount is invalid") from error
        if not math.isfinite(amount) or amount < 0 or amount > 1_000_000:
            raise ValueError("amount is outside the accepted range")

        expected_checksum = hashlib.sha256("".join(canonical_parts).encode("ascii")).hexdigest()
        if not hmac.compare_digest(values["checksum"], expected_checksum):
            raise ValueError("SHA-256 checksum mismatch")

        return NativePlan(
            plan_id=values["id"],
            action=values["action"],
            risk=values["risk"],
            simulated=values["simulated"] == "1",
            approved=values["approved"] == "1",
            amount_cad=amount,
            created_at_utc=values["created_at_utc"],
            checksum=values["checksum"],
        )

    @staticmethod
    def _move(path: Path, destination: Path) -> None:
        target = destination / path.name
        if target.exists():
            if target.read_bytes() != path.read_bytes():
                raise ValueError("destination contains a conflicting plan identifier")
            path.unlink()
            return
        path.replace(target)

    def _reject(self, path: Path, reason: str) -> None:
        safe_reason = reason.replace("\r", " ").replace("\n", " ")[:500]
        target = self.rejected / path.name
        if path.exists() or path.is_symlink():
            if target.exists():
                target = self.rejected / f"{path.stem}.duplicate-rejected{path.suffix}"
            path.replace(target)
            target.with_suffix(target.suffix + ".reason").write_text(
                safe_reason + "\n",
                encoding="ascii",
                errors="replace",
            )
