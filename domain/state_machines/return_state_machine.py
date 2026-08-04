from domain.state_machines.base import StateMachine, Transition

class ReturnStateMachine(StateMachine):
    def __init__(self) -> None:
        super().__init__([
            Transition("requested", "approved", "approve"),
            Transition("requested", "declined", "decline"),
            Transition("approved", "received", "receive"),
            Transition("received", "refunded", "refund"),
            Transition("requested", "cancelled", "cancel")
        ], terminal_states=('declined', 'refunded', 'cancelled'))
