from __future__ import annotations

if __package__ in {None, ""}:
    import sys
    from pathlib import Path as _BootstrapPath
    sys.path.insert(0, str(_BootstrapPath(__file__).resolve().parents[1]))

from pathlib import Path
from tools.runtime_tool import emit
from integrations.shopify.graphql_document_loader import GraphQLDocumentLoader
def main():
 root=Path('integrations/shopify/operations');loader=GraphQLDocumentLoader(root);files=list(root.rglob('*.graphql'));errors=[]
 for p in files:
  try:loader.load(str(p.relative_to(root)))
  except Exception as e:errors.append({'file':str(p),'error':str(e)})
 return emit({'documents':len(files),'errors':errors},0 if not errors else 2)
if __name__=='__main__':raise SystemExit(main())
