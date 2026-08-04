from quality.quality_gate import QualityGate

def test_quality_gate_reports_each_failed_dimension():
    result=QualityGate().evaluate({"media":.9,"supplier":.4},{"media":.8,"supplier":.7})
    assert not result.passed and result.failures==("supplier",)
