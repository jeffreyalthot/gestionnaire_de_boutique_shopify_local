from domain.state_machines.base import StateMachine, Transition

class FulfillmentStateMachine(StateMachine):
    def __init__(self) -> None:
        super().__init__([
            Transition("unfulfilled", "on_hold", "hold"),
            Transition("on_hold", "unfulfilled", "release"),
            Transition("unfulfilled", "in_progress", "start"),
            Transition("in_progress", "fulfilled", "complete"),
            Transition("unfulfilled", "cancelled", "cancel")
        ], terminal_states=('cancelled', 'fulfilled'))
