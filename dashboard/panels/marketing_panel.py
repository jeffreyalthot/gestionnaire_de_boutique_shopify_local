from dashboard.panels.base_panel import PanelField, StatePanel


class MarketingPanel(StatePanel):
    title = 'Marketing'
    fields = (
        PanelField('Campaigns', 'campaigns', 'integer'),
        PanelField('Spend', 'spend_cad', 'money'),
        PanelField('Revenue', 'revenue_cad', 'money'),
        PanelField('ROAS', 'roas', 'ratio'),
    )
