from dashboard.panels.base_panel import PanelField, StatePanel


class ExceptionsPanel(StatePanel):
    title = 'Exceptions'
    fields = (
        PanelField('Open', 'open', 'integer'),
        PanelField('Retry', 'retry', 'integer'),
        PanelField('Dead', 'dead', 'integer'),
        PanelField('Critical', 'critical', 'integer'),
    )
