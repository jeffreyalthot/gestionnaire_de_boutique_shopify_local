from domain.state_machines.payment_state_machine import PaymentStateMachine
def test_payment_transition():
    assert PaymentStateMachine().transition("pending","authorize")=="authorized"
