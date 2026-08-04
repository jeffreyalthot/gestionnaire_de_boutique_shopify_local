from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from pathlib import Path
from tools.runtime_tool import emit
from integrations.shopify.graphql_document_loader import GraphQLDocumentLoader
def main():
 doc=GraphQLDocumentLoader().load('products/query_products.graphql');return emit({'dry_run':True,'operation':doc.split('{',1)[0].strip(),'bytes':len(doc.encode())})
if __name__=='__main__':raise SystemExit(main())
