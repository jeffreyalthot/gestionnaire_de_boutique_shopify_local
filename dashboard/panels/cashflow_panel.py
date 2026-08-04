from dashboard.panels.base_panel import PanelField, StatePanel


class CashflowPanel(StatePanel):
    title = 'Cashflow'
    fields = (
        PanelField('Cash', 'cash_cad', 'money'),
        PanelField('Reserved', 'reserved_cad', 'money'),
        PanelField('Payable', 'payable_cad', 'money'),
        PanelField('Runway', 'runway_days', 'integer'),
    )
