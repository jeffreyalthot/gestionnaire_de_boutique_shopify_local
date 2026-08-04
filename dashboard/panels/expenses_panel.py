from dashboard.panels.base_panel import PanelField, StatePanel


class ExpensesPanel(StatePanel):
    title = 'Expenses'
    fields = (
        PanelField('Supplier', 'supplier_cad', 'money'),
        PanelField('Shipping', 'shipping_cad', 'money'),
        PanelField('Fees', 'fees_cad', 'money'),
        PanelField('Marketing', 'marketing_cad', 'money'),
    )
