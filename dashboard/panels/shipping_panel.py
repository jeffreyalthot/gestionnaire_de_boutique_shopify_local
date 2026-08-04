from dashboard.panels.base_panel import PanelField, StatePanel


class ShippingPanel(StatePanel):
    title = 'Shipping'
    fields = (
        PanelField('Pending', 'pending', 'integer'),
        PanelField('In transit', 'in_transit', 'integer'),
        PanelField('Late', 'late', 'integer'),
        PanelField('Delivered', 'delivered', 'integer'),
    )
