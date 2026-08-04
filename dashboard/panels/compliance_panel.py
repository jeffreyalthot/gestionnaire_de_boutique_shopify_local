from dashboard.panels.base_panel import PanelField, StatePanel


class CompliancePanel(StatePanel):
    title = 'Compliance'
    fields = (
        PanelField('Status', 'status', 'status'),
        PanelField('Passed', 'passed', 'integer'),
        PanelField('Blocked', 'blocked', 'integer'),
        PanelField('Warnings', 'warnings', 'integer'),
    )
