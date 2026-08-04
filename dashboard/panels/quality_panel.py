from dashboard.panels.base_panel import PanelField, StatePanel


class QualityPanel(StatePanel):
    title = 'Quality'
    fields = (
        PanelField('Score', 'score', 'ratio'),
        PanelField('Passed', 'passed', 'integer'),
        PanelField('Failed', 'failed', 'integer'),
        PanelField('Quarantined', 'quarantined', 'integer'),
    )
