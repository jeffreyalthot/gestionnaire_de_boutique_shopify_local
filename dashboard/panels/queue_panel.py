from dashboard.panels.base_panel import PanelField, StatePanel


class QueuePanel(StatePanel):
    title = 'Queues'
    fields = (
        PanelField('Pending', 'pending', 'integer'),
        PanelField('Leased', 'leased', 'integer'),
        PanelField('Completed', 'completed', 'integer'),
        PanelField('Dead', 'dead', 'integer'),
    )
