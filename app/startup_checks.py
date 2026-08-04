from __future__ import annotations
from pathlib import Path
from config.settings import Settings
from infrastructure.database.engine import Database
from security.secret_scanner import scan_tree

def run_startup_checks(settings: Settings,db: Database,project_root: Path) -> dict[str,object]:
    db.initialize()
    findings=[x for x in scan_tree(project_root) if not x[0].endswith(".env.example")]
    checks={
      "database":db.health()["ok"],
      "payment_card_storage_forbidden":settings.payment_data_storage_forbidden,
      "ai_memory_limit":settings.ai_max_ram_mb<=1000,
      "audit_chain":db.verify_audit_chain()["ok"],
      "shopify_configured":settings.live_shopify_ready,
      "alibaba_configured":settings.live_alibaba_ready,
      "secrets_in_repository":not findings,
    }
    required_ok=(checks["database"] and checks["payment_card_storage_forbidden"]
                 and checks["ai_memory_limit"] and checks["audit_chain"]
                 and checks["secrets_in_repository"])
    live_ok=settings.app_dry_run or (settings.live_shopify_ready and settings.live_alibaba_ready)
    return {"ok":required_ok and live_ok,"checks":checks,"secret_findings":findings,
            "mode":"dry_run" if settings.app_dry_run else "live"}
