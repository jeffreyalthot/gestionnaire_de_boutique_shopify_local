from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from infrastructure.database.engine import Database
from infrastructure.native_plan_bridge import NativePlanBridge


def write_plan(
    pending: Path,
    *,
    plan_id: str,
    action: str = "catalog-sync",
    risk: str = "reversible",
    simulated: bool = True,
    approved: bool = False,
    amount_cad: float = 0.0,
) -> Path:
    canonical = (
        "version=1\n"
        f"id={plan_id}\n"
        f"action={action}\n"
        f"risk={risk}\n"
        f"simulated={int(simulated)}\n"
        f"approved={int(approved)}\n"
        f"amount_cad={amount_cad:.2f}\n"
        "created_at_utc=2026-07-29T00:00:00Z\n"
    )
    checksum = hashlib.sha256(canonical.encode("ascii")).hexdigest()
    path = pending / f"{plan_id}.plan"
    path.write_text(canonical + f"checksum={checksum}\n", encoding="ascii")
    return path


class NativePlanBridgeTests(unittest.TestCase):
    def test_imports_valid_simulated_plan_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = Database(root / "runtime.db")
            database.initialize()
            bridge = NativePlanBridge(database, root / "plans")
            plan_id = "a" * 32
            write_plan(bridge.pending, plan_id=plan_id)

            first = bridge.ingest_pending()
            self.assertEqual(first["imported"], 1)
            self.assertTrue((bridge.processed / f"{plan_id}.plan").is_file())
            row = database.query_one("SELECT status FROM native_plans WHERE id=?", (plan_id,))
            self.assertEqual(row["status"], "imported")
            self.assertTrue(database.verify_audit_chain()["ok"])

            second = bridge.ingest_pending()
            self.assertEqual(second["scanned"], 0)

    def test_live_financial_plan_requires_runtime_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = Database(root / "runtime.db")
            database.initialize()
            bridge = NativePlanBridge(database, root / "plans")
            plan_id = "b" * 32
            write_plan(
                bridge.pending,
                plan_id=plan_id,
                action="refund",
                risk="financial",
                simulated=False,
                approved=True,
                amount_cad=50.0,
            )

            result = bridge.ingest_pending()
            self.assertEqual(result["awaiting_approval"], 1)
            approval = database.query_one(
                "SELECT status FROM approvals WHERE entity_type='native_plan' AND entity_id=?",
                (plan_id,),
            )
            self.assertEqual(approval["status"], "pending")
            self.assertTrue((bridge.awaiting_approval / f"{plan_id}.plan").is_file())

    def test_rejects_modified_plan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            database = Database(root / "runtime.db")
            database.initialize()
            bridge = NativePlanBridge(database, root / "plans")
            plan_id = "c" * 32
            path = write_plan(bridge.pending, plan_id=plan_id)
            path.write_text(path.read_text(encoding="ascii").replace("catalog-sync", "refund"), encoding="ascii")

            result = bridge.ingest_pending()
            self.assertEqual(result["rejected"], 1)
            self.assertIsNone(database.query_one("SELECT id FROM native_plans WHERE id=?", (plan_id,)))
            self.assertTrue((bridge.rejected / f"{plan_id}.plan.reason").is_file())


if __name__ == "__main__":
    unittest.main()
