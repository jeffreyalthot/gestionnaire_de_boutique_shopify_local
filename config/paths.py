from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_DIR = DATA_DIR / "database"
BACKUP_DIR = DATA_DIR / "backups"
CACHE_DIR = DATA_DIR / "cache"
LOG_DIR = DATA_DIR / "logs"
REPORT_DIR = DATA_DIR / "reports"
NATIVE_PLAN_DIR = DATA_DIR / "native_plans"
MODEL_DIR = PROJECT_ROOT / "ai" / "model_files"

def ensure_runtime_directories() -> None:
    for path in (DATABASE_DIR, BACKUP_DIR, CACHE_DIR, LOG_DIR, REPORT_DIR, MODEL_DIR / "active",
                 MODEL_DIR / "checkpoints", MODEL_DIR / "rollback", NATIVE_PLAN_DIR / "pending",
                 NATIVE_PLAN_DIR / "processed", NATIVE_PLAN_DIR / "awaiting_approval",
                 NATIVE_PLAN_DIR / "rejected"):
        path.mkdir(parents=True, exist_ok=True)
