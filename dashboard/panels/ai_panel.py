from dashboard.panels.base_panel import PanelField, StatePanel


class AIPanel(StatePanel):
    title = 'AI'
    fields = (
        PanelField('Enabled', 'enabled', 'bool'),
        PanelField('Models', 'models', 'integer'),
        PanelField('Decisions', 'decisions', 'integer'),
        PanelField('Confidence', 'confidence', 'ratio'),
    )
