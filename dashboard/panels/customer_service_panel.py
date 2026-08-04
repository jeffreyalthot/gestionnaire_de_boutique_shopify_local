from dashboard.panels.base_panel import PanelField, StatePanel


class CustomerServicePanel(StatePanel):
    title = 'Customer Service'
    fields = (
        PanelField('Open', 'open', 'integer'),
        PanelField('Overdue', 'overdue', 'integer'),
        PanelField('Escalated', 'escalated', 'integer'),
        PanelField('SLA %', 'sla_percent', 'percent'),
    )
