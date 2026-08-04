from config.settings import get_settings
from infrastructure.database.engine import Database

def main() -> int:
    db=Database(get_settings().database_path); db.initialize()
    missing=db.query("SELECT id,title FROM products WHERE status='published' AND shopify_product_id='' LIMIT 500")
    print({'missing_shopify_product_id':missing}); return 1 if missing else 0
if __name__=='__main__': raise SystemExit(main())
