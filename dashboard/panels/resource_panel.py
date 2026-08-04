from dashboard.panels.base_panel import PanelField, StatePanel


class ResourcePanel(StatePanel):
    title = 'Resources'
    fields = (
        PanelField('CPU', 'cpu_percent', 'percent'),
        PanelField('RAM', 'rss_bytes', 'bytes'),
        PanelField('Threads', 'threads', 'integer'),
        PanelField('Queue pressure', 'queue_pressure', 'ratio'),
    )
