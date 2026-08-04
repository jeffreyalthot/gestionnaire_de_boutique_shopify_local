from dashboard.panels.base_panel import PanelField, StatePanel


class ApiHealthPanel(StatePanel):
    title = 'API Health'
    fields = (
        PanelField('Shopify', 'shopify.status', 'status'),
        PanelField('Alibaba', 'alibaba.status', 'status'),
        PanelField('Database', 'database.status', 'status'),
        PanelField('Latency', 'latency_ms', 'text'),
    )
