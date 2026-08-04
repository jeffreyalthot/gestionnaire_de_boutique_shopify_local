from domain.state_machines.base import StateMachine, Transition

class ShopifyOrderStateMachine(StateMachine):
    def __init__(self) -> None:
        super().__init__([
            Transition("received", "paid", "payment_confirmed"),
            Transition("paid", "queued", "risk_clear"),
            Transition("paid", "risk_review", "risk_high"),
            Transition("risk_review", "queued", "approved"),
            Transition("queued", "procured", "procured"),
            Transition("procured", "fulfilled", "fulfilled"),
            Transition("received", "cancelled", "cancel"),
            Transition("paid", "refunded", "refund")
        ], terminal_states=('cancelled', 'refunded', 'fulfilled'))
