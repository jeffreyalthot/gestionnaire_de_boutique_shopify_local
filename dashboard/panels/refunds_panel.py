from dashboard.panels.base_panel import PanelField, StatePanel


class RefundsPanel(StatePanel):
    title = 'Refunds'
    fields = (
        PanelField('Pending', 'pending', 'integer'),
        PanelField('Approved', 'approved', 'integer'),
        PanelField('Completed', 'completed', 'integer'),
        PanelField('Exposure', 'exposure_cad', 'money'),
    )
