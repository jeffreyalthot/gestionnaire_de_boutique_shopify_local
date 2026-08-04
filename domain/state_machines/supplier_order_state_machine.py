from domain.state_machines.base import StateMachine, Transition

class SupplierOrderStateMachine(StateMachine):
    def __init__(self) -> None:
        super().__init__([
            Transition("pending", "submitted", "submit"),
            Transition("submitted", "paid", "payment_confirmed"),
            Transition("paid", "shipped", "shipped"),
            Transition("shipped", "delivered", "delivered"),
            Transition("pending", "failed", "fail"),
            Transition("submitted", "failed", "fail")
        ], terminal_states=('failed', 'delivered'))
