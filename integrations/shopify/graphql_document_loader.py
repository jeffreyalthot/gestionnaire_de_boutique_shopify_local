from __future__ import annotations
import re
from pathlib import Path
class GraphQLDocumentLoader:
    def __init__(self,root: Path|None=None)->None:self.root=root or Path(__file__).with_name('operations')
    def load(self,path: str)->str:
        target=(self.root/path).resolve()
        if self.root.resolve() not in target.parents or target.suffix!='.graphql':raise ValueError('Document GraphQL hors racine.')
        text=target.read_text(encoding='utf-8').strip()
        if not re.match(r'^(query|mutation|subscription)\s+[A-Za-z_]',text):raise ValueError('Document GraphQL nommé requis.')
        return text
