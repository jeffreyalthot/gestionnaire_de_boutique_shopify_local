import io,json
from integrations.shopify.bulk.jsonl_stream_reader import JsonlStreamReader

def test_bulk_jsonl_is_consumed_incrementally():
    source=io.BytesIO(b"".join((json.dumps({"id":i})+"\n").encode() for i in range(2000)))
    rows=JsonlStreamReader(max_line_bytes=128).read(source)
    assert next(rows)=={"id":0}
    assert sum(1 for _ in rows)==1999
