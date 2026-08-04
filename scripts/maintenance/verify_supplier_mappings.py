from config.settings import get_settings
from infrastructure.database.engine import Database

def main() -> int:
    db=Database(get_settings().database_path); db.initialize()
    missing=db.query("SELECT id,title FROM products WHERE supplier_product_id='' OR supplier_id='' LIMIT 500")
    print({'missing_supplier_mapping':missing}); return 1 if missing else 0
if __name__=='__main__': raise SystemExit(main())
