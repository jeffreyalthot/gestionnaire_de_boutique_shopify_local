from __future__ import annotations
import hashlib
import json
import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterator, Sequence
from uuid import uuid4

from infrastructure.database.sqlite_pragmas import PRAGMAS

_SCHEMA = """
CREATE TABLE IF NOT EXISTS schema_meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  topic TEXT NOT NULL,
  external_id TEXT NOT NULL,
  shop_domain TEXT NOT NULL DEFAULT '',
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  attempts INTEGER NOT NULL DEFAULT 0,
  error TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL,
  processed_at TEXT,
  UNIQUE(source, external_id)
);
CREATE INDEX IF NOT EXISTS idx_events_status_created ON events(status, created_at);

CREATE TABLE IF NOT EXISTS tasks (
  id TEXT PRIMARY KEY,
  queue TEXT NOT NULL,
  task_type TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  priority INTEGER NOT NULL DEFAULT 100,
  status TEXT NOT NULL DEFAULT 'pending',
  attempts INTEGER NOT NULL DEFAULT 0,
  max_attempts INTEGER NOT NULL DEFAULT 8,
  available_at TEXT NOT NULL,
  lease_until TEXT,
  worker_id TEXT,
  idempotency_key TEXT NOT NULL UNIQUE,
  error TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_claim ON tasks(status, queue, available_at, priority);

CREATE TABLE IF NOT EXISTS key_values (
  key TEXT PRIMARY KEY,
  value_json TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY,
  supplier_product_id TEXT NOT NULL UNIQUE,
  shopify_product_id TEXT NOT NULL DEFAULT '',
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  category TEXT NOT NULL DEFAULT '',
  supplier_id TEXT NOT NULL DEFAULT '',
  currency TEXT NOT NULL DEFAULT 'USD',
  supplier_cost REAL NOT NULL DEFAULT 0,
  shipping_cost REAL NOT NULL DEFAULT 0,
  landed_cost_cad REAL NOT NULL DEFAULT 0,
  sale_price_cad REAL NOT NULL DEFAULT 0,
  stock INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'draft',
  score REAL NOT NULL DEFAULT 0,
  data_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);

CREATE TABLE IF NOT EXISTS product_variants (
  id TEXT PRIMARY KEY,
  product_id TEXT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
  supplier_sku_id TEXT NOT NULL,
  shopify_variant_id TEXT NOT NULL DEFAULT '',
  sku TEXT NOT NULL,
  options_json TEXT NOT NULL DEFAULT '{}',
  supplier_cost REAL NOT NULL DEFAULT 0,
  sale_price_cad REAL NOT NULL DEFAULT 0,
  stock INTEGER NOT NULL DEFAULT 0,
  updated_at TEXT NOT NULL,
  UNIQUE(product_id, supplier_sku_id)
);

CREATE TABLE IF NOT EXISTS orders (
  id TEXT PRIMARY KEY,
  shopify_order_id TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  customer_id TEXT NOT NULL DEFAULT '',
  encrypted_shipping_address TEXT NOT NULL DEFAULT '',
  currency TEXT NOT NULL,
  total_amount REAL NOT NULL,
  revenue_cad REAL NOT NULL DEFAULT 0,
  supplier_cost_cad REAL NOT NULL DEFAULT 0,
  shipping_cost_cad REAL NOT NULL DEFAULT 0,
  fees_cad REAL NOT NULL DEFAULT 0,
  profit_cad REAL NOT NULL DEFAULT 0,
  financial_status TEXT NOT NULL,
  fulfillment_status TEXT NOT NULL,
  procurement_status TEXT NOT NULL DEFAULT 'pending',
  risk_level TEXT NOT NULL DEFAULT 'unknown',
  payload_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_orders_procurement ON orders(procurement_status, financial_status);

CREATE TABLE IF NOT EXISTS order_lines (
  id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  shopify_line_id TEXT NOT NULL,
  shopify_variant_id TEXT NOT NULL DEFAULT '',
  sku TEXT NOT NULL,
  supplier_product_id TEXT NOT NULL DEFAULT '',
  supplier_sku_id TEXT NOT NULL DEFAULT '',
  title TEXT NOT NULL,
  quantity INTEGER NOT NULL,
  unit_revenue_cad REAL NOT NULL,
  unit_supplier_cost_cad REAL NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'pending',
  UNIQUE(order_id, shopify_line_id)
);

CREATE TABLE IF NOT EXISTS batches (
  id TEXT PRIMARY KEY,
  status TEXT NOT NULL DEFAULT 'open',
  currency TEXT NOT NULL DEFAULT 'CAD',
  total_cad REAL NOT NULL DEFAULT 0,
  order_count INTEGER NOT NULL DEFAULT 0,
  supplier_count INTEGER NOT NULL DEFAULT 0,
  external_ids_json TEXT NOT NULL DEFAULT '[]',
  error TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  submitted_at TEXT,
  paid_at TEXT
);

CREATE TABLE IF NOT EXISTS batch_orders (
  batch_id TEXT NOT NULL REFERENCES batches(id) ON DELETE CASCADE,
  order_id TEXT NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
  supplier_id TEXT NOT NULL DEFAULT '',
  supplier_order_id TEXT NOT NULL DEFAULT '',
  amount_cad REAL NOT NULL DEFAULT 0,
  PRIMARY KEY(batch_id, order_id)
);

CREATE TABLE IF NOT EXISTS payments (
  id TEXT PRIMARY KEY,
  batch_id TEXT NOT NULL DEFAULT '',
  supplier_order_id TEXT NOT NULL,
  amount REAL NOT NULL,
  currency TEXT NOT NULL,
  status TEXT NOT NULL,
  external_reference TEXT NOT NULL DEFAULT '',
  response_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS shipments (
  id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL,
  supplier_order_id TEXT NOT NULL,
  carrier TEXT NOT NULL DEFAULT '',
  tracking_number TEXT NOT NULL DEFAULT '',
  tracking_url TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'pending',
  events_json TEXT NOT NULL DEFAULT '[]',
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS ledger (
  id TEXT PRIMARY KEY,
  transaction_id TEXT NOT NULL,
  account TEXT NOT NULL,
  debit REAL NOT NULL DEFAULT 0,
  credit REAL NOT NULL DEFAULT 0,
  currency TEXT NOT NULL DEFAULT 'CAD',
  memo TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ledger_transaction ON ledger(transaction_id);

CREATE TABLE IF NOT EXISTS approvals (
  id TEXT PRIMARY KEY,
  action TEXT NOT NULL,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  amount_cad REAL NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'pending',
  requested_at TEXT NOT NULL,
  decided_at TEXT,
  decided_by TEXT NOT NULL DEFAULT '',
  reason TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS ai_decisions (
  id TEXT PRIMARY KEY,
  decision_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  confidence REAL NOT NULL,
  action TEXT NOT NULL,
  features_json TEXT NOT NULL,
  outcome REAL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_log (
  id TEXT PRIMARY KEY,
  action TEXT NOT NULL,
  actor TEXT NOT NULL,
  detail_json TEXT NOT NULL,
  created_at TEXT NOT NULL,
  previous_hash TEXT NOT NULL DEFAULT '',
  entry_hash TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS native_plans (
  id TEXT PRIMARY KEY,
  action TEXT NOT NULL,
  risk TEXT NOT NULL,
  simulated INTEGER NOT NULL,
  approved INTEGER NOT NULL,
  amount_cad REAL NOT NULL DEFAULT 0,
  source_path TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  created_at TEXT NOT NULL,
  ingested_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_native_plans_status ON native_plans(status, ingested_at);

CREATE TABLE IF NOT EXISTS automation_cycles (
  id TEXT PRIMARY KEY,
  status TEXT NOT NULL,
  report_json TEXT NOT NULL DEFAULT '{}',
  started_at TEXT NOT NULL,
  finished_at TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_automation_cycles_started ON automation_cycles(started_at DESC);

CREATE TABLE IF NOT EXISTS automation_actions (
  id TEXT PRIMARY KEY,
  idempotency_key TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  status TEXT NOT NULL,
  result_json TEXT NOT NULL DEFAULT '{}',
  error TEXT NOT NULL DEFAULT '',
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_automation_actions_status ON automation_actions(status, updated_at);

CREATE TABLE IF NOT EXISTS media_assets (
  id TEXT PRIMARY KEY,
  source_url TEXT NOT NULL,
  source_host TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  content_type TEXT NOT NULL,
  byte_size INTEGER NOT NULL,
  width INTEGER NOT NULL DEFAULT 0,
  height INTEGER NOT NULL DEFAULT 0,
  rights_status TEXT NOT NULL DEFAULT 'unverified',
  local_path TEXT NOT NULL DEFAULT '',
  shopify_media_id TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'cached',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  UNIQUE(source_url, sha256)
);
CREATE INDEX IF NOT EXISTS idx_media_assets_status ON media_assets(status, updated_at);

CREATE TABLE IF NOT EXISTS supplier_scores (
  supplier_id TEXT PRIMARY KEY,
  score REAL NOT NULL,
  risk_level TEXT NOT NULL,
  metrics_json TEXT NOT NULL DEFAULT '{}',
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS price_history (
  id TEXT PRIMARY KEY,
  product_id TEXT NOT NULL,
  supplier_cost REAL NOT NULL,
  shipping_cost REAL NOT NULL,
  sale_price REAL NOT NULL,
  currency TEXT NOT NULL DEFAULT 'CAD',
  reason TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_price_history_product ON price_history(product_id, created_at DESC);

CREATE TABLE IF NOT EXISTS customer_tickets (
  id TEXT PRIMARY KEY,
  external_id TEXT NOT NULL DEFAULT '',
  order_id TEXT NOT NULL DEFAULT '',
  customer_id TEXT NOT NULL DEFAULT '',
  category TEXT NOT NULL,
  priority INTEGER NOT NULL DEFAULT 100,
  status TEXT NOT NULL DEFAULT 'open',
  subject TEXT NOT NULL DEFAULT '',
  body_encrypted TEXT NOT NULL DEFAULT '',
  context_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_customer_tickets_queue ON customer_tickets(status, priority, created_at);

CREATE TABLE IF NOT EXISTS reconciliation_checkpoints (
  name TEXT PRIMARY KEY,
  cursor TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'idle',
  detail_json TEXT NOT NULL DEFAULT '{}',
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runtime_snapshots (
  id TEXT PRIMARY KEY,
  snapshot_json TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_runtime_snapshots_created ON runtime_snapshots(created_at DESC);

CREATE TABLE IF NOT EXISTS automation_exceptions (
  id TEXT PRIMARY KEY,
  operation TEXT NOT NULL DEFAULT '',
  category TEXT NOT NULL,
  severity TEXT NOT NULL,
  retryable INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'open',
  message TEXT NOT NULL,
  payload_json TEXT NOT NULL DEFAULT '{}',
  attempts INTEGER NOT NULL DEFAULT 0,
  next_retry_at TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_automation_exceptions_queue
  ON automation_exceptions(status, severity, next_retry_at, created_at);

CREATE TABLE IF NOT EXISTS operation_checkpoints (
  operation TEXT NOT NULL,
  checkpoint_key TEXT NOT NULL,
  state_json TEXT NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'saved',
  updated_at TEXT NOT NULL,
  PRIMARY KEY(operation, checkpoint_key)
);

CREATE TABLE IF NOT EXISTS policy_decisions (
  id TEXT PRIMARY KEY,
  policy TEXT NOT NULL,
  entity_type TEXT NOT NULL DEFAULT '',
  entity_id TEXT NOT NULL DEFAULT '',
  allowed INTEGER NOT NULL,
  score REAL NOT NULL DEFAULT 0,
  reason TEXT NOT NULL DEFAULT '',
  detail_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_policy_decisions_entity ON policy_decisions(entity_type, entity_id, created_at DESC);

CREATE TABLE IF NOT EXISTS reconciliation_runs (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  status TEXT NOT NULL,
  scanned INTEGER NOT NULL DEFAULT 0,
  matched INTEGER NOT NULL DEFAULT 0,
  drifted INTEGER NOT NULL DEFAULT 0,
  repaired INTEGER NOT NULL DEFAULT 0,
  detail_json TEXT NOT NULL DEFAULT '{}',
  started_at TEXT NOT NULL,
  finished_at TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_reconciliation_runs_name ON reconciliation_runs(name, started_at DESC);

CREATE TABLE IF NOT EXISTS metric_facts (
  id TEXT PRIMARY KEY,
  metric TEXT NOT NULL,
  value REAL NOT NULL,
  dimensions_json TEXT NOT NULL DEFAULT '{}',
  observed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_metric_facts_metric ON metric_facts(metric, observed_at DESC);

CREATE TABLE IF NOT EXISTS customer_profiles (
  customer_id TEXT PRIMARY KEY,
  email_hash TEXT NOT NULL DEFAULT '',
  country_code TEXT NOT NULL DEFAULT '',
  language TEXT NOT NULL DEFAULT '',
  lifetime_value_cad REAL NOT NULL DEFAULT 0,
  risk_score REAL NOT NULL DEFAULT 0,
  preferences_json TEXT NOT NULL DEFAULT '{}',
  tags_json TEXT NOT NULL DEFAULT '[]',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS customer_consents (
  id TEXT PRIMARY KEY,
  customer_id TEXT NOT NULL,
  purpose TEXT NOT NULL,
  granted INTEGER NOT NULL,
  source TEXT NOT NULL DEFAULT '',
  evidence_hash TEXT NOT NULL DEFAULT '',
  recorded_at TEXT NOT NULL,
  expires_at TEXT,
  UNIQUE(customer_id, purpose, recorded_at)
);
CREATE INDEX IF NOT EXISTS idx_customer_consents_lookup ON customer_consents(customer_id, purpose, recorded_at DESC);

CREATE TABLE IF NOT EXISTS customer_segment_memberships (
  customer_id TEXT NOT NULL,
  segment TEXT NOT NULL,
  score REAL NOT NULL DEFAULT 0,
  reason TEXT NOT NULL DEFAULT '',
  updated_at TEXT NOT NULL,
  PRIMARY KEY(customer_id, segment)
);

CREATE TABLE IF NOT EXISTS config_revisions (
  revision TEXT PRIMARY KEY,
  files_json TEXT NOT NULL,
  status TEXT NOT NULL,
  detail_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS order_timelines (
  id TEXT PRIMARY KEY,
  order_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT '',
  detail_json TEXT NOT NULL DEFAULT '{}',
  occurred_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_order_timelines_order ON order_timelines(order_id, occurred_at);

CREATE TABLE IF NOT EXISTS inventory_positions (
  sku TEXT NOT NULL,
  location_id TEXT NOT NULL DEFAULT 'default',
  on_hand INTEGER NOT NULL DEFAULT 0,
  reserved INTEGER NOT NULL DEFAULT 0,
  safety_stock INTEGER NOT NULL DEFAULT 0,
  incoming INTEGER NOT NULL DEFAULT 0,
  supplier_available INTEGER,
  updated_at TEXT NOT NULL,
  PRIMARY KEY(sku, location_id)
);

CREATE TABLE IF NOT EXISTS price_snapshots (
  id TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  price_cad REAL NOT NULL,
  landed_cost_cad REAL NOT NULL DEFAULT 0,
  margin_percent REAL NOT NULL DEFAULT 0,
  source TEXT NOT NULL DEFAULT '',
  metadata_json TEXT NOT NULL DEFAULT '{}',
  observed_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_price_snapshots_entity ON price_snapshots(entity_type, entity_id, observed_at DESC);

CREATE TABLE IF NOT EXISTS purchase_intents (
  id TEXT PRIMARY KEY,
  idempotency_key TEXT NOT NULL UNIQUE,
  order_id TEXT NOT NULL,
  supplier_id TEXT NOT NULL,
  amount_cad REAL NOT NULL DEFAULT 0,
  currency TEXT NOT NULL DEFAULT 'CAD',
  status TEXT NOT NULL DEFAULT 'planned',
  payload_json TEXT NOT NULL DEFAULT '{}',
  external_order_id TEXT NOT NULL DEFAULT '',
  error TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_purchase_intents_status ON purchase_intents(status, created_at);

CREATE TABLE IF NOT EXISTS risk_decisions (
  id TEXT PRIMARY KEY,
  entity_type TEXT NOT NULL,
  entity_id TEXT NOT NULL,
  score REAL NOT NULL,
  level TEXT NOT NULL,
  held INTEGER NOT NULL,
  reasons_json TEXT NOT NULL DEFAULT '[]',
  detail_json TEXT NOT NULL DEFAULT '{}',
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_risk_decisions_entity ON risk_decisions(entity_type, entity_id, created_at DESC);

CREATE TABLE IF NOT EXISTS oauth_states (
  state_hash TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  redirect_uri TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL,
  expires_at TEXT NOT NULL,
  consumed_at TEXT
);

CREATE TABLE IF NOT EXISTS credential_versions (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL,
  key_name TEXT NOT NULL,
  fingerprint TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TEXT NOT NULL,
  retired_at TEXT
);
CREATE INDEX IF NOT EXISTS idx_credential_versions_active ON credential_versions(provider, key_name, status);
"""

def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()

class Database:
    def __init__(self, path: Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._local = threading.local()
        self._write_lock = threading.RLock()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path, timeout=10, isolation_level=None, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        for pragma in PRAGMAS:
            conn.execute(pragma)
        return conn

    def initialize(self) -> None:
        with self.connect() as conn:
            conn.executescript(_SCHEMA)
            audit_columns = {str(row["name"]) for row in conn.execute("PRAGMA table_info(audit_log)")}
            if "previous_hash" not in audit_columns:
                conn.execute("ALTER TABLE audit_log ADD COLUMN previous_hash TEXT NOT NULL DEFAULT ''")
            if "entry_hash" not in audit_columns:
                conn.execute("ALTER TABLE audit_log ADD COLUMN entry_hash TEXT NOT NULL DEFAULT ''")
            conn.execute(
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_audit_entry_hash "
                "ON audit_log(entry_hash) WHERE entry_hash <> ''"
            )
            previous_hash = "0" * 64
            rows = conn.execute(
                "SELECT rowid,id,action,actor,detail_json,created_at,previous_hash,entry_hash "
                "FROM audit_log ORDER BY rowid ASC"
            ).fetchall()
            for row in rows:
                if row["previous_hash"] and row["entry_hash"]:
                    previous_hash = str(row["entry_hash"])
                    continue
                entry_hash = self._audit_hash(
                    previous_hash,
                    str(row["id"]),
                    str(row["action"]),
                    str(row["actor"]),
                    str(row["detail_json"]),
                    str(row["created_at"]),
                )
                conn.execute(
                    "UPDATE audit_log SET previous_hash=?,entry_hash=? WHERE rowid=?",
                    (previous_hash, entry_hash, row["rowid"]),
                )
                previous_hash = entry_hash
            conn.execute("INSERT OR REPLACE INTO schema_meta(key,value) VALUES('version','5')")

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        with self._write_lock:
            conn = self.connect()
            try:
                conn.execute("BEGIN IMMEDIATE")
                yield conn
                conn.execute("COMMIT")
            except BaseException:
                conn.execute("ROLLBACK")
                raise
            finally:
                conn.close()

    def execute(self, sql: str, params: Sequence[Any] = ()) -> int:
        with self.transaction() as conn:
            cur = conn.execute(sql, params)
            return cur.rowcount

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[dict[str, Any]]:
        with self.connect() as conn:
            return [dict(row) for row in conn.execute(sql, params).fetchall()]

    def query_one(self, sql: str, params: Sequence[Any] = ()) -> dict[str, Any] | None:
        rows = self.query(sql, params)
        return rows[0] if rows else None

    def scalar(self, sql: str, params: Sequence[Any] = (), default: Any = None) -> Any:
        with self.connect() as conn:
            row = conn.execute(sql, params).fetchone()
            return row[0] if row is not None else default

    def set_value(self, key: str, value: Any) -> None:
        self.execute(
            "INSERT INTO key_values(key,value_json,updated_at) VALUES(?,?,?) "
            "ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=excluded.updated_at",
            (key, json.dumps(value, ensure_ascii=False, default=str), utcnow()),
        )

    def get_value(self, key: str, default: Any = None) -> Any:
        row = self.query_one("SELECT value_json FROM key_values WHERE key=?", (key,))
        return json.loads(row["value_json"]) if row else default

    def insert_event(self, source: str, topic: str, external_id: str, payload: dict[str, Any],
                     shop_domain: str = "") -> bool:
        try:
            self.execute(
                "INSERT INTO events(id,source,topic,external_id,shop_domain,payload_json,created_at) VALUES(?,?,?,?,?,?,?)",
                (str(uuid4()), source, topic, external_id, shop_domain,
                 json.dumps(payload, ensure_ascii=False, default=str), utcnow()),
            )
            return True
        except sqlite3.IntegrityError:
            return False

    def mark_event(self, external_id: str, status: str, error: str = "") -> None:
        self.execute(
            "UPDATE events SET status=?,error=?,attempts=attempts+1,processed_at=? WHERE external_id=?",
            (status, error, utcnow(), external_id),
        )

    @staticmethod
    def _audit_hash(
        previous_hash: str,
        record_id: str,
        action: str,
        actor: str,
        detail_json: str,
        created_at: str,
    ) -> str:
        material = "\n".join((previous_hash, record_id, action, actor, detail_json, created_at))
        return hashlib.sha256(material.encode("utf-8")).hexdigest()

    def insert_audit(self, action: str, actor: str, detail: dict[str, Any]) -> str:
        record_id = str(uuid4())
        created_at = utcnow()
        detail_json = json.dumps(detail, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
        with self.transaction() as conn:
            previous = conn.execute(
                "SELECT entry_hash FROM audit_log ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
            previous_hash = str(previous["entry_hash"]) if previous and previous["entry_hash"] else "0" * 64
            entry_hash = self._audit_hash(
                previous_hash,
                record_id,
                action,
                actor,
                detail_json,
                created_at,
            )
            conn.execute(
                "INSERT INTO audit_log(id,action,actor,detail_json,created_at,previous_hash,entry_hash) "
                "VALUES(?,?,?,?,?,?,?)",
                (record_id, action, actor, detail_json, created_at, previous_hash, entry_hash),
            )
        return record_id

    def verify_audit_chain(self) -> dict[str, Any]:
        rows = self.query(
            "SELECT rowid,id,action,actor,detail_json,created_at,previous_hash,entry_hash "
            "FROM audit_log ORDER BY rowid ASC"
        )
        previous_hash = "0" * 64
        for index, row in enumerate(rows):
            expected = self._audit_hash(
                previous_hash,
                str(row["id"]),
                str(row["action"]),
                str(row["actor"]),
                str(row["detail_json"]),
                str(row["created_at"]),
            )
            if row["previous_hash"] != previous_hash or row["entry_hash"] != expected:
                return {
                    "ok": False,
                    "entries": len(rows),
                    "invalid_index": index,
                    "invalid_id": str(row["id"]),
                }
            previous_hash = expected
        return {"ok": True, "entries": len(rows), "head": previous_hash}

    def register_native_plan(
        self,
        *,
        plan_id: str,
        action: str,
        risk: str,
        simulated: bool,
        approved: bool,
        amount_cad: float,
        source_path: str,
        payload: dict[str, Any],
    ) -> bool:
        try:
            self.execute(
                "INSERT INTO native_plans(id,action,risk,simulated,approved,amount_cad,source_path,"
                "payload_json,status,created_at,ingested_at) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                (
                    plan_id,
                    action,
                    risk,
                    int(simulated),
                    int(approved),
                    amount_cad,
                    source_path,
                    json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":")),
                    "pending",
                    str(payload["created_at_utc"]),
                    utcnow(),
                ),
            )
            return True
        except sqlite3.IntegrityError:
            return False

    def set_native_plan_status(self, plan_id: str, status: str) -> None:
        allowed = {"pending", "imported", "awaiting_approval", "approved", "rejected", "completed"}
        if status not in allowed:
            raise ValueError("Statut de plan natif invalide.")
        self.execute("UPDATE native_plans SET status=? WHERE id=?", (status, plan_id))

    def request_native_plan_approval(self, plan_id: str, action: str, amount_cad: float) -> str:
        approval_id = f"native-plan-{plan_id}"
        self.execute(
            "INSERT OR IGNORE INTO approvals(id,action,entity_type,entity_id,amount_cad,status,requested_at) "
            "VALUES(?,?, 'native_plan', ?, ?, 'pending', ?)",
            (approval_id, action, plan_id, amount_cad, utcnow()),
        )
        return approval_id

    def health(self) -> dict[str, Any]:
        started = datetime.now(timezone.utc)
        result = self.scalar("SELECT 1", default=0)
        latency = (datetime.now(timezone.utc) - started).total_seconds() * 1000
        return {"ok": result == 1, "latency_ms": round(latency, 2), "path": str(self.path)}

    def financial_snapshot(self) -> dict[str, float]:
        row = self.query_one(
            "SELECT COALESCE(SUM(revenue_cad),0) revenue, COALESCE(SUM(supplier_cost_cad),0) supplier_cost,"
            " COALESCE(SUM(shipping_cost_cad),0) shipping, COALESCE(SUM(fees_cad),0) fees,"
            " COALESCE(SUM(profit_cad),0) profit FROM orders WHERE financial_status IN ('paid','partially_refunded')"
        ) or {}
        return {k: float(row.get(k, 0)) for k in ("revenue", "supplier_cost", "shipping", "fees", "profit")}

    def counts(self) -> dict[str, int]:
        return {
            "orders": int(self.scalar("SELECT COUNT(*) FROM orders", default=0)),
            "paid_orders": int(self.scalar("SELECT COUNT(*) FROM orders WHERE financial_status='paid'", default=0)),
            "pending_procurement": int(self.scalar(
                "SELECT COUNT(*) FROM orders WHERE financial_status='paid' AND procurement_status='pending'", default=0)),
            "products": int(self.scalar("SELECT COUNT(*) FROM products", default=0)),
            "active_products": int(self.scalar("SELECT COUNT(*) FROM products WHERE status='active'", default=0)),
            "open_batches": int(self.scalar("SELECT COUNT(*) FROM batches WHERE status IN ('open','ready','approval_required')", default=0)),
            "pending_tasks": int(self.scalar("SELECT COUNT(*) FROM tasks WHERE status IN ('pending','leased')", default=0)),
            "failed_tasks": int(self.scalar("SELECT COUNT(*) FROM tasks WHERE status='dead'", default=0)),
            "alerts": int(self.scalar("SELECT COUNT(*) FROM approvals WHERE status='pending'", default=0)),
        }

    def purge_expired_leases(self) -> int:
        return self.execute(
            "UPDATE tasks SET status='pending',worker_id=NULL,lease_until=NULL,updated_at=? "
            "WHERE status='leased' AND lease_until < ?",
            (utcnow(), utcnow()),
        )
