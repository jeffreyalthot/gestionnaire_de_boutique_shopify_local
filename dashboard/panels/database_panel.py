from dashboard.panels.base_panel import PanelField, StatePanel


class DatabasePanel(StatePanel):
    title = 'Database'
    fields = (
        PanelField('Status', 'status', 'status'),
        PanelField('Size', 'size_bytes', 'bytes'),
        PanelField('WAL', 'wal_bytes', 'bytes'),
        PanelField('Integrity', 'integrity', 'status'),
    )
