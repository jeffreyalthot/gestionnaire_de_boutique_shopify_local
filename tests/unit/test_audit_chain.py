from __future__ import annotations

import tempfile
import unittest
import sqlite3
from pathlib import Path

from infrastructure.database.engine import Database


class AuditChainTests(unittest.TestCase):
    def test_chain_detects_detail_tampering(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Database(Path(directory) / "audit.db")
            database.initialize()
            database.insert_audit("first", "test", {"value": 1})
            database.insert_audit("second", "test", {"value": 2})

            valid = database.verify_audit_chain()
            self.assertTrue(valid["ok"])
            self.assertEqual(valid["entries"], 2)

            first = database.query_one("SELECT id FROM audit_log ORDER BY rowid ASC LIMIT 1")
            self.assertIsNotNone(first)
            database.execute(
                "UPDATE audit_log SET detail_json='{\"value\":999}' WHERE id=?",
                (first["id"],),
            )

            invalid = database.verify_audit_chain()
            self.assertFalse(invalid["ok"])
            self.assertEqual(invalid["invalid_index"], 0)

    def test_legacy_rows_are_chained_once(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "legacy.db"
            with sqlite3.connect(path) as connection:
                connection.execute(
                    "CREATE TABLE audit_log("
                    "id TEXT PRIMARY KEY,action TEXT NOT NULL,actor TEXT NOT NULL,"
                    "detail_json TEXT NOT NULL,created_at TEXT NOT NULL)"
                )
                connection.execute(
                    "INSERT INTO audit_log(id,action,actor,detail_json,created_at) "
                    "VALUES('legacy','import','test','{}','2026-07-29T00:00:00+00:00')"
                )
            database = Database(path)
            database.initialize()
            self.assertTrue(database.verify_audit_chain()["ok"])
            columns = {row["name"] for row in database.query("PRAGMA table_info(audit_log)")}
            self.assertIn("previous_hash", columns)
            self.assertIn("entry_hash", columns)


if __name__ == "__main__":
    unittest.main()
