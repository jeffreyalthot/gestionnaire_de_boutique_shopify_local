from domain.state_machines.base import StateMachine, Transition

class PaymentStateMachine(StateMachine):
    def __init__(self) -> None:
        super().__init__([
            Transition("pending", "authorized", "authorize"),
            Transition("authorized", "paid", "capture"),
            Transition("pending", "failed", "fail"),
            Transition("authorized", "failed", "fail"),
            Transition("paid", "refunded", "refund")
        ], terminal_states=('failed', 'refunded'))
