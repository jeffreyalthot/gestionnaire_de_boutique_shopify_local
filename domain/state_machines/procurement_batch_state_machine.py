from domain.state_machines.base import StateMachine, Transition

class ProcurementBatchStateMachine(StateMachine):
    def __init__(self) -> None:
        super().__init__([
            Transition("open", "ready", "threshold_reached"),
            Transition("ready", "approval_required", "approval_required"),
            Transition("ready", "submitting", "submit"),
            Transition("approval_required", "submitting", "approved"),
            Transition("submitting", "submitted", "success"),
            Transition("submitting", "partial", "partial"),
            Transition("submitting", "failed", "fail"),
            Transition("submitted", "paid", "paid")
        ], terminal_states=('failed', 'paid'))
