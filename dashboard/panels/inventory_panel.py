from dashboard.panels.base_panel import PanelField, StatePanel


class InventoryPanel(StatePanel):
    title = 'Inventory'
    fields = (
        PanelField('Units', 'units', 'integer'),
        PanelField('Reserved', 'reserved', 'integer'),
        PanelField('Incoming', 'incoming', 'integer'),
        PanelField('Low stock', 'low_stock', 'integer'),
    )
