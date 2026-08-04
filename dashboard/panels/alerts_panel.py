from dashboard.panels.base_panel import PanelField, StatePanel


class AlertsPanel(StatePanel):
    title = 'Alerts'
    fields = (
        PanelField('Open', 'open', 'integer'),
        PanelField('Critical', 'critical', 'integer'),
        PanelField('Suppressed', 'suppressed', 'integer'),
        PanelField('Last', 'last', 'text'),
    )
