from dashboard.panels.base_panel import PanelField, StatePanel


class RuntimePanel(StatePanel):
    title = 'Runtime'
    fields = (
        PanelField('Status', 'status', 'status'),
        PanelField('Cycles', 'cycles', 'integer'),
        PanelField('Completed', 'completed', 'integer'),
        PanelField('Failed', 'failed', 'integer'),
    )
