from dashboard.panels.base_panel import PanelField, StatePanel


class PaymentsPanel(StatePanel):
    title = 'Payments'
    fields = (
        PanelField('Pending', 'pending', 'integer'),
        PanelField('Completed', 'completed', 'integer'),
        PanelField('Failed', 'failed', 'integer'),
        PanelField('Exposure', 'exposure_cad', 'money'),
    )
