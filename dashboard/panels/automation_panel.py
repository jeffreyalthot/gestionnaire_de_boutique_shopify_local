from dashboard.panels.base_panel import PanelField, StatePanel


class AutomationPanel(StatePanel):
    title = 'Automation'
    fields = (
        PanelField('Phase', 'phase', 'status'),
        PanelField('Planned', 'planned', 'integer'),
        PanelField('Completed', 'completed', 'integer'),
        PanelField('Failed', 'failed', 'integer'),
        PanelField('Deferred', 'deferred', 'integer'),
    )
