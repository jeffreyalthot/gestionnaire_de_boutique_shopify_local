import pytest
from security.pci_guard import reject_payment_card_data
def test_card_data_rejected():
    with pytest.raises(ValueError): reject_payment_card_data({"cvv":"123"})
