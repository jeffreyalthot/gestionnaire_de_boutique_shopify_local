from __future__ import annotations
from collections import defaultdict
from integrations.shopify.bulk.jsonl_stream_reader import JsonlStreamReader
class BulkResultImporter:
    def __init__(self,handler,max_line_bytes: int=8*1024*1024)->None:self.handler=handler;self.reader=JsonlStreamReader(max_line_bytes)
    def import_file(self,path)->dict[str,int]:
        counts=defaultdict(int)
        for record in self.reader.read(path):
            kind=str(record.get('__typename') or record.get('type') or 'unknown');self.handler(record);counts[kind]+=1
        return dict(counts)
