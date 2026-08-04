from integrations.alibaba.permission_probe import CAPABILITY_METHODS
def test_required_methods(): assert CAPABILITY_METHODS["payment"]=="alibaba.dropshipping.order.pay"
