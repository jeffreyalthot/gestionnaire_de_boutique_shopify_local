from dashboard.panels.base_panel import PanelField, StatePanel


class ProcurementPanel(StatePanel):
    title = 'Procurement'
    fields = (
        PanelField('Batches', 'batches', 'integer'),
        PanelField('Orders', 'orders', 'integer'),
        PanelField('Awaiting approval', 'awaiting_approval', 'integer'),
        PanelField('Spend', 'spend_cad', 'money'),
    )
