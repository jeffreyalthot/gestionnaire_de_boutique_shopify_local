from dashboard.panels.base_panel import PanelField, StatePanel


class SupplierPanel(StatePanel):
    title = 'Suppliers'
    fields = (
        PanelField('Active', 'active', 'integer'),
        PanelField('High risk', 'high_risk', 'integer'),
        PanelField('Average score', 'average_score', 'ratio'),
        PanelField('Open RFQ', 'open_rfq', 'integer'),
    )
