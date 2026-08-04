from dashboard.panels.base_panel import PanelField, StatePanel


class OrdersPanel(StatePanel):
    title = 'Orders'
    fields = (
        PanelField('Total', 'orders', 'integer'),
        PanelField('Paid', 'paid', 'integer'),
        PanelField('Risk holds', 'risk_holds', 'integer'),
        PanelField('Pending procurement', 'pending_procurement', 'integer'),
    )
