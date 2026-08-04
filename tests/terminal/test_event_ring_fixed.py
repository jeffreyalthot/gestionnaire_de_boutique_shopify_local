from dashboard.log_ring_buffer import LogRingBuffer

def test_event_ring_never_grows_beyond_reserved_rows():
    ring=LogRingBuffer(3)
    for i in range(20): ring.append(str(i))
    assert len(ring.lines())==3 and ring.lines()[-1].endswith("19")
