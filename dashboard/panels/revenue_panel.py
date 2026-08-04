from dashboard.panels.base_panel import PanelField, StatePanel


class RevenuePanel(StatePanel):
    title = 'Revenue'
    fields = (
        PanelField('Today', 'today_cad', 'money'),
        PanelField('Week', 'week_cad', 'money'),
        PanelField('Month', 'month_cad', 'money'),
        PanelField('Orders', 'orders', 'integer'),
    )
