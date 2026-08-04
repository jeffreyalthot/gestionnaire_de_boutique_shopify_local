from dashboard.panels.base_panel import PanelField, StatePanel


class ProfitPanel(StatePanel):
    title = 'Profit'
    fields = (
        PanelField('Revenue', 'revenue_cad', 'money'),
        PanelField('Gross profit', 'gross_profit_cad', 'money'),
        PanelField('Net profit', 'net_profit_cad', 'money'),
        PanelField('Margin', 'margin_percent', 'percent'),
    )
